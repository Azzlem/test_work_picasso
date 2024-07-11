from rest_framework import serializers

from bicycle_rental.models import Bicycle, Rental


class BicycleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bicycle
        fields = ('id', 'name',)


class BicycleRentalStartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = (
            'bicycle',
        )


class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ('id', 'user', 'bicycle', 'datetime_rented', 'datetime_rented_stop')
