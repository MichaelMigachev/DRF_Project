# from django.urls import path
from rest_framework.routers import DefaultRouter

from users.apps import UsersConfig
from users.views import CourseViewSet

# Описание маршрутизации для User

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'', CourseViewSet, basename='users')

urlpatterns = [] + router.urls