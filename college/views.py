# from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from college.models import Course, Lesson
from college.serliazers import CourseSerializer, LessonSerializer
from college.paginators import CustomPagination
from college.tasks import send_email_to_subs_after_updating_course

from users.permissions import IsModerator, IsOwner

# Create your views here.


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def get_permissions(self):
        """Возвращает список разрешений, требуемых для пользователей группы moderators."""
        if self.action == "create":
            self.permission_classes = (IsAuthenticated & ~IsModerator,)
        elif self.action in ["update", "retrieve", "list"]:
            self.permission_classes = (
                IsAuthenticated & IsOwner | IsModerator,
            )
        elif self.action == "destroy":
            self.permission_classes = (IsAuthenticated & IsOwner,)
        return super().get_permissions()

    def perform_update(self, serializer):
        """Переопределение метода для отправки сообщения об обновлении курса"""
        instance = serializer.save()
        send_email_to_subs_after_updating_course.delay(instance.pk)


class LessonCreteAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated & ~IsModerator,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        # new_lesson = serializer.save()
        # new_lesson.owner = self.request.user
        # new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated & IsModerator | IsOwner,)
    pagination_class = CustomPagination

    def get_queryset(self):
        """Возвращает объекты в зависимости от прав доступа."""
        if self.request.user.groups.filter(name="moderators"):
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user.pk)


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated & IsModerator | IsOwner,)


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated & IsOwner,)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated & IsModerator | IsOwner,)
