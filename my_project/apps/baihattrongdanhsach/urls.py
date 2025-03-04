from django.urls import path
from .views import them_bai_hat, them_bai_hat_vao_danhsach, xoa_bai_hat_khoi_danhsach

urlpatterns = [
    path('baihat/them/', them_bai_hat, name='them_bai_hat'),
    path('danhsachphat/them-baihat/', them_bai_hat_vao_danhsach, name='them_bai_hat_vao_danhsach'),

    path('danhsachphat/xoa-baihat/', xoa_bai_hat_khoi_danhsach, name='xoa_bai_hat_khoi_danhsach'),

]
