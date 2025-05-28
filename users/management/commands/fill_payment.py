from django.core.management.base import BaseCommand
from college.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    help = "Create payment records for all users"

    def handle(self, *args, **options):
        payment_for_create = []

        for user in User.objects.all():
            payment_for_create.append(
                Payment(
                    user=user,
                    paid_lesson=Lesson.objects.get(pk=2),
                    amount=5000,
                    payment_method="cash",
                )
            )

        for user in User.objects.all():
            payment_for_create.append(
                Payment(
                    user=user,
                    paid_course=Course.objects.get(pk=2),
                    amount=10000,
                    payment_method="transfer",
                )
            )

        Payment.objects.bulk_create(payment_for_create)
