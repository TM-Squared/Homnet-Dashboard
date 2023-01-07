from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import login_view, register_user
app_name = "account"

urlpatterns = [
    path('login', login_view, name="login"),
    path('register', register_user, name="register"),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
]