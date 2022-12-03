from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import login_view, register_user

app_name = "account"

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout")
]