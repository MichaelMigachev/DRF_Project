from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "phone_number",)
    # list_display = ("id", "email", "username", "phone_number", "avatar", "city")
    search_fields = ("email", "phone_number")
