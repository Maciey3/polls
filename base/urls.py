from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('poll/<int:pk>/', views.poll, name="poll"),
    path('create-poll/', views.create_poll, name="create-poll"),
    path('update-poll/<int:pk>/', views.update_poll, name="update-poll"),
    path('delete-poll/<int:pk>/', views.delete_poll, name="delete-poll"),
]