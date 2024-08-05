from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from user.views import CreateUserView

urlpatterns = [
    path("token", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token-refresh"),
    path("register", CreateUserView.as_view(), name="register"),
]

app_name = "user"
