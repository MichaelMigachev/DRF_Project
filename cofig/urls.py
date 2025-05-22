from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('college.urls', namespace='college')),
    path("users/", include("users.urls", namespace="users")),
]
