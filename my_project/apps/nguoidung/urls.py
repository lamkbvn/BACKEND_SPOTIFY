from django.urls import path
from .views import them_nguoi_dung, cap_nhat_nguoi_dung, login, logout, refresh_token, request_password_reset, \
    password_reset_confirm, danh_sach_nguoi_dung, chi_tiet_nguoi_dung, khoa_tai_khoan

urlpatterns = [
    path('api/them-nguoi-dung/', them_nguoi_dung, name='them-nguoi-dung'),
    path('api/cap-nhat-nguoi-dung', cap_nhat_nguoi_dung, name='cap-nhat-nguoi-dung'),
    path('api/dang-nhap' ,  login ,  name = 'dang-nhap'),
    path('api/dang-xuat' ,  logout ,  name = 'dang-xuat'),
    path('api/refresh-token' ,  refresh_token ,  name = 'refresh-token'),
    path('api/forgot-password' ,  request_password_reset  , name = 'forgot-password') ,
    path('api/forgot-password/<uidb64>/<token>/', password_reset_confirm, name='password-reset-confirm'),
    path('api/danh-sach-nguoi-dung/', danh_sach_nguoi_dung, name='danh-sach-nguoi-dung'),
    path('api/chi-tiet-nguoi-dung/<int:nguoi_dung_id>/', chi_tiet_nguoi_dung, name='chi-tiet-nguoi-dung'),
    path('api/khoa-tai-khoan/<int:nguoi_dung_id>/lock/', khoa_tai_khoan, name='khoa-tai-khoan'),
]


