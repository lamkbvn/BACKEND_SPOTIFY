from django.urls import path
from .views import get_loaibaihat, them_loaibaihat, get_loaibaihat_by_id, update_loaibaihat, delete_loaibaihat

urlpatterns = [
    path('', get_loaibaihat, name='get_loaibaihat'),
    path('them/', them_loaibaihat, name='them_loaibaihat'),
    path('<int:id>/', get_loaibaihat_by_id, name='get_loaibaihat_by_id'),
    path('capnhat/<int:id>/', update_loaibaihat, name='update_loaibaihat'),
    path('xoa/<int:id>/', delete_loaibaihat, name='delete_loaibaihat'),
]
