from django.urls import path
from .views import top_songs

urlpatterns = [
    path('api/top_songs/', top_songs, name='top_songs'),
]
