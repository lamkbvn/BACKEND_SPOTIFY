from django.urls import path
from .views import them_album, get_albums, get_album_by_id, update_album, delete_album, get_album_phan_trang

urlpatterns = [
    path("", get_albums, name="get_albums"),
    path("search/", get_album_phan_trang, name="get_album_phan_trang"),
    path("them/", them_album, name="them_album"),
    path("<int:album_id>/", get_album_by_id, name="get_album_by_id"),
    path("capnhat/<int:album_id>/", update_album, name="update_album"),
    path("xoa/<int:album_id>/", delete_album, name="delete_album"),
]
