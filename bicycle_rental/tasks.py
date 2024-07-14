from celery import shared_task
from django.utils import timezone
from .models import Rental


@shared_task
def calculate_rental_cost(rental_id):
    try:
        rental = Rental.objects.get(id=rental_id)
        if rental.datetime_rented_stop:
            duration = rental.datetime_rented_stop - rental.datetime_rented
            # Предположим, что стоимость аренды равна 10 единиц за час
            cost_per_min = Rental.trip_price_per_min
            total_cost = duration.total_seconds() / 60 * cost_per_min
            rental.trip_price_total = round(total_cost, 2)
            rental.save()
            return total_cost
        else:
            return "Rental is still active"
    except Rental.DoesNotExist:
        return "Rental not found"
