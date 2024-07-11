from django.db import models

from users.models import User


class Bicycle(models.Model):
    name = models.CharField(max_length=50)
    rental_bicycle = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} - {self.rental_bicycle}'

    class Meta:
        verbose_name = 'Bicycle'
        verbose_name_plural = 'Bicycles'


class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bicycle = models.ForeignKey(Bicycle, on_delete=models.CASCADE)
    datetime_rented = models.DateTimeField(auto_now_add=True)
    datetime_rented_stop = models.DateTimeField(default=None, null=True)

    def __str__(self):
        return f'{self.user} - {self.bicycle} - {self.datetime_rented} - {self.datetime_rented_stop}'

    class Meta:
        verbose_name = 'Rental'
        verbose_name_plural = 'Rentals'

