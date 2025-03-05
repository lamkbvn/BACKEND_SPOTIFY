from django.urls import path
from .views import get_loibaihatdongbo, them_loibaihatdongbo, get_loibaihatdongbo_by_id, update_loibaihatdongbo, delete_loibaihatdongbo

urlpatterns = [
    path('', get_loibaihatdongbo, name='get_loibaihatdongbo'),  # Lấy tất cả
    path('them/', them_loibaihatdongbo, name='them_loibaihatdongbo'),  # Thêm mới
    path('<int:id>/', get_loibaihatdongbo_by_id, name='get_loibaihatdongbo_by_id'),  # Lấy theo ID
    path('capnhat/<int:id>/', update_loibaihatdongbo, name='update_loibaihatdongbo'),  # Cập nhật
    path('xoa/<int:id>/', delete_loibaihatdongbo, name='delete_loibaihatdongbo'),  # Xóa
]
