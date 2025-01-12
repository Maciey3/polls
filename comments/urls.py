from django.urls import path
from . import views

urlpatterns = [
    path('create-comment/<int:poll_id>', views.create, name="create-comment"),
    path('vote-comment/<int:comment_id>/<int:vote>', views.htmx_vote, name='vote-comment'),

]