from django.urls import path
from .views import create_zalopay_order, zalopay_callback

urlpatterns = [
    path("zalopay/create/", create_zalopay_order, name="create_zalopay_order"),
    path("zalopay/callback/", zalopay_callback, name="zalopay_callback"),
]
