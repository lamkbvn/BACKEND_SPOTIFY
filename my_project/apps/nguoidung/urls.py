from django.urls import path
from .views import them_nguoi_dung

urlpatterns = [
    path('api/them-nguoi-dung/', them_nguoi_dung, name='them-nguoi-dung'),
]
