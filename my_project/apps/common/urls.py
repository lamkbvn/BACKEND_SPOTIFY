from django.urls import path

from .views import search

urlpatterns = [
    path('api/search', search, name='search'),

]


