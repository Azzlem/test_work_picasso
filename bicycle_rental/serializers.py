from rest_framework import serializers

from bicycle_rental.models import Bicycle, Rental


class BicycleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bicycle
        fields = ('id', 'name',)


class BicycleRentalStartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ['bicycle']

    bicycle = serializers.PrimaryKeyRelatedField(queryset=Bicycle.objects.filter(rental_bicycle=False))


class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ('id', 'user', 'bicycle', 'datetime_rented', 'datetime_rented_stop')


class RentalToUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = "__all__"
