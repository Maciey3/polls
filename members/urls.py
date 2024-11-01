from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_page, name="login"),
    path('register_page', views.register_page, name="register-page"),
    path('register', views.register, name="register"),
    path('logout', views.logout_user, name="logout"),
    path('profile', views.profile, name="members.profile"),
    path('profile/update', views.profile_update, name="members.profile-update"),
]