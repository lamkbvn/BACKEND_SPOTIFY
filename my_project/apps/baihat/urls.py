# urls.py
from django.urls import path
from .views import them_baihat, get_baihat, get_baihat_by_id, get_loi_bai_hat,update_baihat, delete_baihat

urlpatterns = [
    path('baihat/', get_baihat, name='get_baihat'),
    path('baihat/<int:id>/', get_baihat_by_id, name='get_baihat_by_id'),
    path('loibaihat/<int:id>/', get_loi_bai_hat, name='get_loi_bai_hat'),
    path('baihat/them/', them_baihat, name='them_baihat'),
    path('baihat/capnhat/<int:id>/', update_baihat, name='update_baihat'),
    path('baihat/xoa/<int:id>/', delete_baihat, name='delete_baihat'),
]
