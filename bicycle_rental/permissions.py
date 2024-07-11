from rest_framework import permissions

from bicycle_rental.models import Rental
from rest_framework.exceptions import PermissionDenied


class CustomPermissionDenied(PermissionDenied):
    default_detail = "Вы не можете взять второй велосипед в прокат."


class NoBicycle(permissions.BasePermission):
    def has_permission(self, request, view):
        rental_exists = Rental.objects.filter(user=request.user.id, datetime_rented_stop=None).exists()
        if rental_exists:
            raise CustomPermissionDenied()
        else:
            return True


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
