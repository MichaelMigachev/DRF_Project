from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user_list = [
            {"email": "user1@sky.pro", "phone_number": "+70000088888"},
            {"email": "user2@sky.pro", "phone_number": "+78888811111"},
        ]
        user_for_create = []
        for user_item in user_list:
            user_for_create.append(User(**user_item))

        # print(user_for_create)

        User.objects.bulk_create(user_for_create)
