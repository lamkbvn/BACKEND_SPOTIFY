import time
import hmac
import hashlib
import json
import uuid
import requests
from datetime import datetime
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

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