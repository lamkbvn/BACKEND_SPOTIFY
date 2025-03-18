import time
import hmac
import hashlib
import json
import uuid
import requests
from datetime import datetime
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import urllib.parse
from django.http import JsonResponse

ZALOPAY_CONFIG = {
    "appid": 2554,
    "key1": "sdngKKJmqEMzvh5QQcdD2A9XBSKUNaYn",
    "key2": "trMrHtvjo6myautxDUiAcYsVtaeQ8nhf",
    "endpoint": "https://sandbox.zalopay.com.vn/v001/tpe/createorder"
}

@api_view(["POST"])
@permission_classes([AllowAny])
def create_zalopay_order(request):
    try:
        data = request.data
        amount = int(data.get("amount", 50000))  # Lấy số tiền từ request

        # Tạo thông tin đơn hàng
        order = {
            "appid": ZALOPAY_CONFIG["appid"],
            "apptransid": "{:%y%m%d}_{}".format(datetime.today(), uuid.uuid4()),  # Định dạng: yyMMdd_xxxx
            "appuser": "demo",
            "apptime": int(time.time() * 1000),  # Milliseconds
            "embeddata": json.dumps({"merchantinfo": "embeddata123"}, separators=(',', ':')),
            "item": json.dumps([{"itemid": "knb", "itemname": "kim nguyen bao", "itemprice": amount, "itemquantity": 1}], separators=(',', ':')),
            "amount": amount,
            "description": "ZaloPay Integration Demo",
            "bankcode": "zalopayapp"
        }

        # Tạo chữ ký MAC
        data_sign = "{}|{}|{}|{}|{}|{}|{}".format(
            order["appid"], order["apptransid"], order["appuser"],
            order["amount"], order["apptime"], order["embeddata"], order["item"]
        )
        order["mac"] = hmac.new(ZALOPAY_CONFIG["key1"].encode(), data_sign.encode(), hashlib.sha256).hexdigest()

        # Gửi request lên ZaloPay
        response = requests.post(ZALOPAY_CONFIG["endpoint"], data=order)

        if response.status_code != 200:
            return Response({"error": "Invalid response from ZaloPay", "detail": response.text}, status=400)

        return Response(response.json())  # Trả về JSON response từ ZaloPay

    except Exception as e:
        return Response({"error": str(e)}, status=400)
@api_view(["POST"])
@permission_classes([AllowAny])
def zalopay_callback(request):
    try:
        data = request.data
        return_code = data.get("return_code", -1)
        if return_code == 1:
            # Xử lý khi thanh toán thành công (Cập nhật trạng thái đơn hàng)
            return Response({"return_code": 1, "return_message": "Success"})
        return Response({"return_code": -1, "return_message": "Failure"})
    except Exception as e:
        return Response({"return_code": -1, "return_message": str(e)})


import hashlib
import hmac
import urllib.parse
import random
from datetime import datetime
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt

# Hàm lấy địa chỉ IP của client
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# Hàm tạo chữ ký HMAC SHA512
def hmac_sha512(key, data):
    byteKey = key.encode('utf-8')
    byteData = data.encode('utf-8')
    return hmac.new(byteKey, byteData, hashlib.sha512).hexdigest()

# API tạo URL thanh toán VNPay
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def create_vnpay_payment_url(request):
    # Lấy thông tin cấu hình từ settings
    vnp_TmnCode = settings.VNPAY_CONFIG["VNPAY_TMNCODE"]
    vnp_HashSecret = settings.VNPAY_CONFIG["VNPAY_HASH_SECRET"]
    vnp_ReturnUrl = settings.VNPAY_CONFIG["VNPAY_RETURN_URL"]
    vnp_PaymentUrl = settings.VNPAY_CONFIG["VNPAY_URL"]

    # Kiểm tra phương thức request
    if request.method != "POST":
        return JsonResponse({"error": "Phương thức không hợp lệ, chỉ chấp nhận POST"}, status=405)

    # Lấy dữ liệu từ request
    data = request.data
    amount = data.get("amount")  # Số tiền (VND)
    order_id = data.get("order_id")  # Mã đơn hàng

    # Kiểm tra dữ liệu bắt buộc
    if not amount or not order_id:
        return JsonResponse({"error": "Thiếu tham số bắt buộc (amount hoặc order_id)"}, status=400)

    # Lấy địa chỉ IP của client
    ipaddr = get_client_ip(request)

    # Tạo các tham số gửi đến VNPay
    vnp_params = {
        "vnp_Version": "2.1.0",
        "vnp_Command": "pay",
        "vnp_TmnCode": vnp_TmnCode,
        "vnp_Amount": str(int(amount) * 100),  # Nhân 100 để đổi sang đơn vị VND
        "vnp_CurrCode": "VND",
        "vnp_TxnRef": str(order_id),
        "vnp_OrderInfo": f"Thanh toán đơn hàng {order_id}",
        "vnp_OrderType": "other",
        "vnp_Locale": "vn",
        "vnp_ReturnUrl": vnp_ReturnUrl,
        "vnp_CreateDate": datetime.now().strftime('%Y%m%d%H%M%S'),
        "vnp_IpAddr": ipaddr,
        "vnp_BankCode" :  "VNPAYQR"
    }


    # Sắp xếp tham số theo thứ tự ASCII
    sorted_params = sorted(vnp_params.items())

    # Tạo chuỗi query string (mã hóa giá trị)
    query_string = ""
    has_data = ""
    seq = 0
    for key, val in sorted_params:
        if seq == 1:
            query_string += "&" + key + "=" + urllib.parse.quote_plus(str(val))
            has_data += "&" + key + "=" + str(val)  # Dùng giá trị không mã hóa cho chữ ký
        else:
            seq = 1
            query_string += key + "=" + urllib.parse.quote_plus(str(val))
            has_data += key + "=" + str(val)  # Dùng giá trị không mã hóa cho chữ ký

    # Tạo chữ ký HMAC-SHA512
    secure_hash = hmac_sha512(vnp_HashSecret, has_data)

    # Tạo URL thanh toán hoàn chỉnh
    payment_url = f"{vnp_PaymentUrl}?{query_string}&vnp_SecureHash={secure_hash}"

    # Log để debug
    print(f"Hash Data (Create): {has_data}")
    print(f"Payment URL: {payment_url}")

    # Trả về URL trong JSON
    return JsonResponse({"payment_url": payment_url}, status=200)


