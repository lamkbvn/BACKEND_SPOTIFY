from django.urls import path
from .views import them_thanh_toan, get_thanh_toan, get_thanh_toan_by_id, update_thanh_toan, delete_thanh_toan, lock_thanh_toan, unlock_thanh_toan

urlpatterns = [
    path('thanhtoan', them_thanh_toan, name='them_thanhtoan'),  # Thêm thanh toán (POST)
    path('thanhtoan/list/', get_thanh_toan, name='get_thanhtoan'),  # Lấy danh sách thanh toán (GET)
    path('thanhtoan/<int:id>', get_thanh_toan_by_id, name='get_thanhtoan_by_id'),  # Lấy thanh toán theo ID (GET)
    path('thanhtoan/update/<int:id>', update_thanh_toan, name='update_thanhtoan'),  # Cập nhật thanh toán (PUT)
    path('thanhtoan/delete/<int:id>', delete_thanh_toan, name='delete_thanhtoan'),  # Xóa thanh toán (DELETE)
    path('thanhtoan/lock/<int:id>', lock_thanh_toan, name='lock_thanhtoan'),  # Khóa thanh toán (PATCH)
    path('thanhtoan/unlock/<int:id>', unlock_thanh_toan, name='unlock_thanhtoan')  # Mở khóa thanh toán (PATCH)
]