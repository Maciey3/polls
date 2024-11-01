from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('poll/<int:pk>/', views.poll, name="poll"),
    path('poll/<int:pk>/vote', views.vote, name="vote"),
    path('poll/<int:pk>/delete-vote', views.delete_vote, name="delete-vote"),
    path('create-poll/', views.create_poll, name="create-poll"),
    path('store-poll/', views.store_poll, name="store-poll"),
    path('edit-poll/<int:pk>/', views.edit_poll, name="edit-poll"),
    path('update-poll/<int:pk>/', views.update_poll, name="update-poll"),
    path('delete-poll/<int:pk>/', views.delete_poll, name="delete-poll"),
]