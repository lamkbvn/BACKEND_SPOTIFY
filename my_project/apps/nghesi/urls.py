from django.urls import path
from .views import them_nghesi, get_nghesi, get_nghesi_by_id, update_nghesi, delete_nghesi, lock_nghesi, unlock_nghesi, get_so_luong_nghe_si

urlpatterns = [
    path('nghesi', them_nghesi, name='them_nghesi'),  # Thêm nghệ sĩ (POST)
    path('nghesi/list/', get_nghesi, name='get_nghesi'),  # Lấy danh sách nghệ sĩ (GET)
    path('nghesi/<int:id>', get_nghesi_by_id, name='get_nghesi_by_id'),  # Lấy nghệ sĩ theo ID (GET)
    path('nghesi/update/<int:id>', update_nghesi, name='update_nghesi'),  # Cập nhật nghệ sĩ (PUT)
    path('nghesi/delete/<int:id>', delete_nghesi, name='delete_nghesi'), 
    path('nghesi/lock/<int:id>', lock_nghesi, name='lock_nghesi'),# Xóa nghệ sĩ (DELETE)
    path('nghesi/unlock/<int:id>', unlock_nghesi, name='unlock_nghesi'),
    path('nghesi/get-so-luong-nghe-si/', get_so_luong_nghe_si , name='get_so_luong_nghe_si')
]