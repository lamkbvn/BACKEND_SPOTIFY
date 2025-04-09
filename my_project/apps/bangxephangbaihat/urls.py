from django.urls import path
from .views import top_songs, get_all_loai_bang_xep_hang_as_playlist, get_danh_sach_bai_hat_theo_bxh_name, get_bang_xep_hang_theo_loai

urlpatterns = [
    path('api/top_songs/', top_songs, name='top_songs'),
    path('api/get_bxh/', get_all_loai_bang_xep_hang_as_playlist, name='get_bxh'),
    path('api/get_baihat_inBXH/<str:ten_baxh>/', get_danh_sach_bai_hat_theo_bxh_name, name='get_baihat_inBXH'),
    path('api/get_BXH_theoten/<str:ten_bxh>/', get_bang_xep_hang_theo_loai, name='get_BXH_theoten'),
]
