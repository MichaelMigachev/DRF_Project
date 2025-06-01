from django.db import models
from django.conf import settings

# from users.models import User


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name="название")
    preview = models.ImageField(
        upload_to="product/photo",
        blank=True,
        null=True,
        verbose_name="фото",
        help_text="Загрузите фотографию",
    )
    description = models.TextField(
        max_length=250, verbose_name="описание", help_text="Введите описание"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Владелец",
        help_text="Укажите владельца",
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name="название")
    description = models.TextField(
        max_length=250, verbose_name="описание", help_text="Введите описание"
    )
    preview = models.ImageField(
        upload_to="product/photo",
        blank=True,
        null=True,
        verbose_name="фото",
        help_text="Загрузите фотографию",
    )
    video_url = models.URLField(null=True, blank=True, verbose_name="Ссылка на видео")
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Владелец",
        help_text="Укажите владельца",
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
