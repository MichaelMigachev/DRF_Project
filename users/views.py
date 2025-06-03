# from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.models import User, Payment
from users.serliazers import UserSerializer, PaymentSerializer, UserProfilePublicSerializer

# Create your views here.


# class UserViewSet(viewsets.ModelViewSet):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()


class PaymentList(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = {
        "paid_course": ["exact"],
        "paid_lesson": ["exact"],
        "payment_method": ["exact"],
    }
    ordering_fields = ["payment_date"]
    ordering = ["payment_date"]


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        # Возвращает только пользователя, который соответствует текущему аутентифицированному пользователю
        return User.objects.filter(id=self.request.user.id)


class UserDestroyAPIView(DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


# class UserListAPIView(ListAPIView):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()

class UserListAPIView(ListAPIView):
    """
    Позволяет пользователям просматривать список пользователей,
    показывая свой профиль с полными данными и чужие профили с ограниченной информацией.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.all()  # Получает всех пользователей

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        user = request.user
        # Проверка если это свой профиль
        users_data = []
        for user_instance in queryset:
            if user_instance.id == user.id:
                # Если это текущий пользователь, используем полный сериализатор
                serializer = UserSerializer(user_instance)
            else:
                # Иначе используем публичный сериализатор
                serializer = UserProfilePublicSerializer(user_instance)
            users_data.append(serializer.data)

        return Response(users_data)  # Возвращаем комбинированные данные