from django.urls import path
from rest_framework.routers import DefaultRouter

from users.apps import UsersConfig
from users.views import UserViewSet, PaymentList

# Описание маршрутизации для User

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"", UserViewSet, basename="users")

urlpatterns = [
    path("payments/", PaymentList.as_view(), name="payment_list"),
] + router.urls
