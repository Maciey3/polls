from django.urls import path
from . import views

urlpatterns = [
    path('create-comment/<int:poll_id>', views.create, name="create-comment"),
]