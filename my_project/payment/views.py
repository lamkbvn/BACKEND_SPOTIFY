import logging
import time
import hmac
import hashlib
import json
import uuid
import requests
from datetime import datetime, timedelta
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import urllib.parse
from django.http import JsonResponse
import paypalrestsdk
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from apps.common.serializers import ThanhToanSerializer
from apps.thanhtoan.views import them_thanh_toan  # Nếu ở cùng thư mục
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from apps.thanhtoan.views import them_thanh_toan_internal
ZALOPAY_CONFIG = {
    "appid": 2554,
    "key1": "sdngKKJmqEMzvh5QQcdD2A9XBSKUNaYn",
    "key2": "trMrHtvjo6myautxDUiAcYsVtaeQ8nhf",
    "endpoint": "https://sandbox.zalopay.com.vn/v001/tpe/createorder"
}
PAYPAL_CONFIG = {
"PAYPAL_CLIENT_ID": "AZ_-6YwdsonLLP-tlZe6eZPSgI_0qLxZjq4ETlICSlHX6TT5eoJOEIm1uRNKddRhER8i6ZxH8EN0-1li",
"PAYPAL_CLIENT_SECRET": "ENj2tLvl0OBZ9abzGCkVbh2EClzfGpSvvvCd_y1fITKI-RbzVSQkEM1ZIf2FhQqDOnnV-jcIQ9x0DmMw"
}

logger = logging.getLogger(__name__)

@api_view(["POST"])
@permission_classes([AllowAny])
def create_zalopay_order(request):
    try:
        logger.info(f"Received request data: {request.data}")
        data = request.data
        amount = int(data.get("amount", 50000))  # Lấy số tiền từ request
        user_id = data.get("user_id")
        
        if not user_id:
            logger.error("Missing user_id in request")
            return Response({"error": "user_id is required"}, status=400)

        logger.info(f"Creating order for user_id: {user_id}, amount: {amount}")
        
        # Tạo thông tin đơn hàng
        order = {
            "appid": ZALOPAY_CONFIG["appid"],
            "apptransid": "{:%y%m%d}_{}".format(datetime.today(), uuid.uuid4()),
            "appuser": str(user_id),
            "apptime": int(time.time() * 1000),
            "embeddata": json.dumps({"merchantinfo": "embeddata123"}, separators=(',', ':')),
            "item": json.dumps([{"itemid": "knb", "itemname": "kim nguyen bao", "itemprice": amount, "itemquantity": 1}], separators=(',', ':')),
            "amount": amount,
            "description": "ZaloPay Integration Demo",
            "bankcode": ""
        }

        # Tạo chữ ký MAC
        data_sign = "{}|{}|{}|{}|{}|{}|{}".format(
            order["appid"], order["apptransid"], order["appuser"],
            order["amount"], order["apptime"], order["embeddata"], order["item"]
        )
        order["mac"] = hmac.new(ZALOPAY_CONFIG["key1"].encode(), data_sign.encode(), hashlib.sha256).hexdigest()

        logger.info(f"Sending order to ZaloPay: {order}")
        
        # Gửi request lên ZaloPay
        response = requests.post(ZALOPAY_CONFIG["endpoint"], data=order)
        response_data = response.json()
        logger.info(f"ZaloPay response: status_code={response.status_code}, data={response_data}")

        # Kiểm tra kết quả từ ZaloPay
        if response.status_code == 200 and response_data.get("returncode") == 1:
            logger.info("ZaloPay transaction successful, saving payment data")
            goi_premium_id = 1
            so_ngay_hieu_luc = 30

            thanh_toan_data = {
                "nguoi_dung": user_id,
                "goi_premium": goi_premium_id,
                "so_tien": amount,
                "phuong_thuc": "ZaloPay",
                "ngay_thanh_toan": timezone.now(),
                "ngay_het_han": timezone.now() + timedelta(days=so_ngay_hieu_luc),
                "tu_dong_gia_han": False,
                "is_active": True
            }

            serializer = ThanhToanSerializer(data=thanh_toan_data)
            if serializer.is_valid():
                serializer.save()
                logger.info("Payment data saved successfully")
                return Response(response_data)
            else:
                logger.error(f"Serializer errors: {serializer.errors}")
                return Response({"error": "Failed to save payment", "detail": serializer.errors}, status=400)

        logger.error(f"ZaloPay transaction failed: {response_data}")
        return Response({"error": "ZaloPay transaction failed", "detail": response_data}, status=400)

    except ValueError as e:
        logger.error(f"ValueError: {str(e)} - Likely invalid amount")
        return Response({"error": "Invalid amount value"}, status=400)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return Response({"error": str(e)}, status=400)
@api_view(["POST"])
@permission_classes([AllowAny])
def zalopay_callback(request):
    try:
        data = request.data
        print(data)
        return_code = data.get("returncode", -1)
        appuser = data.get("appuser")  # Lấy user_id từ appuser
        amount = data.get("amount", 0)
        if return_code == 1 and appuser:
            from datetime import timedelta
            # Giả sử appuser là ID người dùng và gói premium mặc định là ID 1
            goi_premium_id = 1  # ID của gói premium, bạn có thể lấy từ request hoặc đặt mặc định
            so_ngay_hieu_luc = 30  # Ví dụ: gói premium có hiệu lực 30 ngày

            thanh_toan_data = {
                "nguoi_dung": appuser,  # ID người dùng
                "goi_premium": goi_premium_id,  # Gói premium
                "so_tien": amount,
                "phuong_thuc": "ZaloPay",
                "ngay_thanh_toan": timezone.now(),
                "ngay_het_han": timezone.now() + timedelta(days=so_ngay_hieu_luc),
                "tu_dong_gia_han": False,  # Hoặc lấy từ request nếu có
                "is_active": True  # Thanh toán thành công => active
            }

            serializer = ThanhToanSerializer(data=thanh_toan_data)
            if serializer.is_valid():
                response = them_thanh_toan(request=Request(request, data=thanh_toan_data))
                return Response({"return_code": 1, "return_message": "Success"})
            else:
                return Response({"return_code": -1, "return_message": serializer.errors})

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





paypalrestsdk.configure({
    "mode": "sandbox",  # Đổi thành "live" khi Go Live
    "client_id": PAYPAL_CONFIG.get("PAYPAL_CLIENT_ID"),
    "client_secret": PAYPAL_CONFIG.get("PAYPAL_CLIENT_SECRET")
})



@csrf_exempt
def capture_paypal_order(request):
    if request.method == 'POST':
        print("➡️ Received POST request to capture PayPal payment.")
        try:
            data = json.loads(request.body)
            print(f"📦 Request data: {data}")
            payment_id = data.get('paymentId')
            payer_id = data.get('payerId')
            print(f"🔍 Payment ID: {payment_id}")
            print(f"🙋‍♂️ Payer ID: {payer_id}")

            print("🔄 Finding payment by ID...")
            payment = paypalrestsdk.Payment.find(payment_id)

            print("💳 Executing payment...")
            if payment.execute({"payer_id": payer_id}):
                print("✅ Payment executed successfully.")
                return JsonResponse({"message": "Payment successful"})
            else:
                print(f"❌ Payment execution failed: {payment.error}")
                return JsonResponse({"error": payment.error}, status=400)
        except Exception as e:
            print(f"❗ Exception occurred: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
      

@csrf_exempt
def create_paypal_order(request):
    if request.method == 'POST':
        print("➡️ Received POST request to create PayPal order.")
        try:
            data = json.loads(request.body)
            amount = data.get('amount')
            idNguoiDung = data.get('idNguoiDung')

            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {"payment_method": "paypal"},
                "redirect_urls": {
                    "return_url": 'http://localhost:8000/api/paypal/success?idNguoiDung='+idNguoiDung,  # frontend
                    "cancel_url": "http://localhost:5173/premium"
                },
                "transactions": [{
                    "amount": {
                        "total": str(amount),
                        "currency": "USD"
                    },
                    "description": "Payment description"
                }]
            })

            if payment.create():
                for link in payment.links:
                    if link.rel == "approval_url":
                        print(f"➡️ Returning approval URL: {link.href}")
                        return JsonResponse({"approval_url": link.href})
                print("⚠️ No approval_url found in payment.links.")
                return JsonResponse({"error": "No approval URL found."}, status=400)
            else:
                print(f"❌ Payment creation failed: {payment.error}")
                return JsonResponse({"error": payment.error}, status=400)
        except Exception as e:
            print(f"❗ Exception occurred: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
          
from django.shortcuts import redirect
@csrf_exempt
def paypal_success(request):
    if request.method == 'GET':
        try:
            payment_id = request.GET.get('paymentId')
            payer_id = request.GET.get('PayerID')
            idNguoiDung = request.GET.get('idNguoiDung')


            if not payment_id or not payer_id:
                return JsonResponse({"error": "Missing paymentId or PayerID"}, status=400)

            # Lấy thông tin thanh toán từ PayPal
            payment = paypalrestsdk.Payment.find(payment_id)

            if payment.execute({"payer_id": payer_id}):

                # Gọi hàm lưu thông tin thanh toán
                xu_ly_thanh_toan_paypal(payment_id, payer_id, idNguoiDung)
                
                 # Redirect về trang chính sau khi thanh toán thành công
                # Truyền thông báo thành công thông qua URL hoặc session
                return redirect(f'http://localhost:5173/premium?success=true&idNguoiDung={idNguoiDung}')
            else:
                print(f"❌ Payment execution failed: {payment.error}")
                return JsonResponse({"error": payment.error}, status=400)
        except Exception as e:
            print(f"❗ Error processing PayPal payment: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

from apps.common.models import NguoiDung, GoiPremium, ThanhToan


def xu_ly_thanh_toan_paypal(payment_id, payer_id, user_id):
    """
    Xử lý thanh toán sau khi nhận phản hồi từ PayPal
    """
    try:
        # Retrieve user and premium package
        nguoi_dung = NguoiDung.objects.get(nguoi_dung_id=user_id)
       
        goi_premium = GoiPremium.objects.get(goi_premium_id=1)  # Assume gói mặc định with id 1
        
        # Calculate expiration date for the package (assuming 30 days for premium)
        ngay_hien_tai = datetime.now()
        ngay_het_han = ngay_hien_tai + timedelta(days=goi_premium.thoi_han)
        
        # Prepare payment data
        payment_data = {
            "nguoi_dung": nguoi_dung,  # Use the actual user object
            "goi_premium": goi_premium,  # Use the actual premium package object
            "phuong_thuc": "PayPal",
            "so_tien": goi_premium.gia,  # Assuming 'gia' is the price
            "ngay_het_han": ngay_het_han,
            "tu_dong_gia_han": False,
            "is_active": True,
        }

        # Save the payment information
        payment = ThanhToan.objects.create(**payment_data)
        nguoi_dung.is_premium = True
        nguoi_dung.save()
        return {"status": "success", "message": "Thanh toán thành công!"}
    
    except NguoiDung.DoesNotExist:
        print("❌ Người dùng không tồn tại")
        return {"status": "error", "message": "Người dùng không tồn tại"}
    
    except GoiPremium.DoesNotExist:
        print("❌ Gói Premium không tồn tại")
        return {"status": "error", "message": "Gói Premium không tồn tại"}
    
    except Exception as e:
        print(f"❗ Error processing payment: {str(e)}")
        return {"status": "error", "message": str(e)}