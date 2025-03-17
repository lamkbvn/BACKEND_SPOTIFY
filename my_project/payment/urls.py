from django.urls import path
from .views import create_zalopay_order, zalopay_callback, create_paypal_order, capture_paypal_order

urlpatterns = [
    path("zalopay/create/", create_zalopay_order, name="create_zalopay_order"),
    path("zalopay/callback/", zalopay_callback, name="zalopay_callback"),
    path("paypal/create/", create_paypal_order, name="create_paypal_order"),
    path("paypal/capture/", capture_paypal_order, name="capture_paypal_order"),
]
