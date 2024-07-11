import os

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email=os.getenv('SUPERUSER_EMAIL'),
            name=os.getenv('SUPERUSER_NAME'),
            is_staff=True,
            is_superuser=True
        )

        user.set_password(os.getenv('SUPERUSER_PASSWORD'))
        user.save()
