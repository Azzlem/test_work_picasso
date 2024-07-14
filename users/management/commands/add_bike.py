from django.core.management import BaseCommand
import os

from bicycle_rental.models import Bicycle


class Command(BaseCommand):

    def handle(self, *args, **options):
        bikes = os.getenv('bikes').split(",")
        for bike in bikes:
            new_bike = Bicycle.objects.create(name=bike)
            new_bike.save()
