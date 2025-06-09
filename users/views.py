from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, status
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListAPIView,
    get_object_or_404,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from college.models import Course, Lesson
from users.models import User, Payment, Follow, Donation
from users.serliazers import UserSerializer, PaymentSerializer, UserProfilePublicSerializer, FollowSerializer, DonationSerializer
from users.services import convert_rub_to_usd, create_stripe_product, create_stripe_price, create_stripe_session

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
    serializer_class = UserSerializer

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
                # serializer = UserSerializer(user_instance)
            users_data.append(serializer.data)

        return Response(users_data)  # Возвращаем комбинированные данные


class FollowUpdateAPIView(UpdateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("id")
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Follow.objects.filter(user=user, courses=course_item)

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
            status_code = status.HTTP_200_OK
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            # subs_item.create()
            Follow.objects.create(user=user, courses=course_item)
            message = "подписка добавлена"
            status_code = status.HTTP_201_CREATED

        # Возвращаем ответ в API
        return Response({"message": message}, status=status_code)


class DonationCreateAPIView(CreateAPIView):
    serializer_class = DonationSerializer
    queryset = Donation.objects.all()
    # permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        course = Course.objects.get(pk=int(self.request.data.get('course')))
        payment = serializer.save(user=self.request.user)
        amount_in_dollars = convert_rub_to_usd(payment.amount)
        product = create_stripe_product(course)
        price = create_stripe_price(amount_in_dollars, product)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


