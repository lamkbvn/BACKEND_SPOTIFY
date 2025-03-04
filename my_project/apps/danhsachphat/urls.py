from django.urls import path
from .views import them_danhsachphat, get_danhsachphat, get_danhsachphat_by_id, update_danhsachphat, delete_danhsachphat

urlpatterns = [
    path('danhsachphat/', get_danhsachphat, name='get_danhsachphat'),
    path('danhsachphat/<int:id>/', get_danhsachphat_by_id, name='get_danhsachphat_by_id'),
    path('danhsachphat/them/', them_danhsachphat, name='them_danhsachphat'),
    path('danhsachphat/capnhat/<int:id>/', update_danhsachphat, name='update_danhsachphat'),
    path('danhsachphat/xoa/<int:id>/', delete_danhsachphat, name='delete_danhsachphat'),
]
