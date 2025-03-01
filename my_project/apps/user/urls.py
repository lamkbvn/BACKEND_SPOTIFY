from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_user, name='create_user'),
    path('update/<int:id>/' , views.update_user , name='update_user'),
]
