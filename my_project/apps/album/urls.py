from django.urls import path
from .views import them_album, get_albums, get_album_by_id, update_album, delete_album, get_album_phan_trang, create_album, get_albums_by_user, get_album_cho_duyet_co_nguoi_dung

urlpatterns = [
    path("", get_albums, name="get_albums"),
    path("search/", get_album_phan_trang, name="get_album_phan_trang"),
    path("them/", them_album, name="them_album"),
    path("<int:album_id>/", get_album_by_id, name="get_album_by_id"),
    path("capnhat/<int:album_id>/", update_album, name="update_album"),
    path("xoa/<int:album_id>/", delete_album, name="delete_album"),
    
    
    path('create/', create_album, name='create_album'),
    path("user/<int:user_id>/", get_albums_by_user, name="get_albums_by_user"),
    path("albumpending/", get_album_cho_duyet_co_nguoi_dung, name="get_album_cho_duyet_co_nguoi_dung"),
   
    
]
