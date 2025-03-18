from django.urls import path
from .views import create_zalopay_order, zalopay_callback, create_vnpay_payment_url

urlpatterns = [
    path("zalopay/create/", create_zalopay_order, name="create_zalopay_order"),
    path("zalopay/callback/", zalopay_callback, name="zalopay_callback"),
    path("vnpay/create_payment/", create_vnpay_payment_url, name="create_payment"),
]
