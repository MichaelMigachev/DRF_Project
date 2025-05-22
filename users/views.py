from django.shortcuts import render
from rest_framework import viewsets
from users.models import User
from users.serliazers import UserSerializer


# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
