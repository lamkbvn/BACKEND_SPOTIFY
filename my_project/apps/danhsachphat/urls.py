from django.urls import path
from .views import them_danhsachphat, get_danhsachphat, get_danhsachphat_by_id, update_danhsachphat, delete_danhsachphat

urlpatterns = [
    path('', get_danhsachphat, name='get_danhsachphat'),
    path('<int:id>/', get_danhsachphat_by_id, name='get_danhsachphat_by_id'),
    path('them/', them_danhsachphat, name='them_danhsachphat'),
    path('capnhat/<int:id>/', update_danhsachphat, name='update_danhsachphat'),
    path('xoa/<int:id>/', delete_danhsachphat, name='delete_danhsachphat'),
]
