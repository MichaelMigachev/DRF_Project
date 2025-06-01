from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny

from users.apps import UsersConfig
from users.views import UserCreateAPIView, PaymentList

# Описание маршрутизации для User

app_name = UsersConfig.name


urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("payments/", PaymentList.as_view(), name="payment_list"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
]
