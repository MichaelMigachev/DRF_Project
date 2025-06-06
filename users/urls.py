from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny

from users.apps import UsersConfig
from users.views import (
    UserCreateAPIView,
    UserUpdateAPIView,
    UserDestroyAPIView,
    UserListAPIView,
    PaymentList,
    FollowUpdateAPIView
)

# Описание маршрутизации для User

app_name = UsersConfig.name


urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("payments/", PaymentList.as_view(), name="payment_list"),
    path("login/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="login",),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh",),

    # CRUD для пользователей
    path("", UserListAPIView.as_view(), name="user_list"),  # Список пользователей
    path("update/<int:pk>/", UserUpdateAPIView.as_view(), name="user_update"),  # Обновление пользователя
    path("delete/<int:pk>/", UserDestroyAPIView.as_view(), name="user_destroy"),  # Удаление пользователя

    # для подписок на курсы
    path("follow/<int:pk>/", FollowUpdateAPIView.as_view(), name="follow_check"),
]
