# from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, filters

from users.models import User, Payment
from users.serliazers import UserSerializer, PaymentSerializer

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


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
