from celery import shared_task
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from config import settings
from college.models import Course

from users.models import Follow

@shared_task
def send_email_to_subs_after_updating_course(course_pk):
    """Функция отправки сообщения об обновлении курса подписчикам."""
    print("Рассылка запущена")
    course = get_object_or_404(Course, pk=course_pk)
    subs = Follow.objects.filter(courses=course)
    if subs:
        print("Рассылка запущена")
        send_mail(
            subject=f"Обновление курса {course.title}",
            message=f"Здравствуйте! Курс {course.title} обновлен! Скорее посмотрите, что изменилось!",
            from_email=settings.EMAIL_HOST_USER,
            # recipient_list=[sub.user.email for sub in subs],
            recipient_list=['7107cert@mail.ru'],
        )
        print("Рассылка завершена")