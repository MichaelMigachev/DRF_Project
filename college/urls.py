from django.urls import path
from rest_framework.routers import DefaultRouter

from college.apps import CollegeConfig
from college.views import (
    CourseViewSet,
    LessonCreteAPIView,
    LessonDestroyAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
)

app_name = CollegeConfig.name

router = DefaultRouter()
router.register(r"course", CourseViewSet, basename="course")

urlpatterns = [
    path("lesson/crete/", LessonCreteAPIView.as_view(), name="lesson_crete"),
    path("lesson/list/", LessonListAPIView.as_view(), name="lesson_list"),
    path(
        "lesson/retriv/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_retriv"
    ),
    path(
        "lesson/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lesson_update"
    ),
    path(
        "lesson/destroy/<int:pk>/",
        LessonDestroyAPIView.as_view(),
        name="lesson_destroy",
    ),
] + router.urls
