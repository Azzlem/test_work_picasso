from django.utils import timezone
from rest_framework import generics, serializers, request, status
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from bicycle_rental.models import Bicycle, Rental
from bicycle_rental.permissions import NoBicycle
from bicycle_rental.serializers import BicycleListSerializer, BicycleRentalStartSerializer, RentalSerializer
from users.models import User


class BicycleListView(generics.ListAPIView):
    queryset = Bicycle.objects.all().filter(rental_bicycle=False)
    serializer_class = BicycleListSerializer


class BicycleStartRentalView(generics.CreateAPIView):
    serializer_class = BicycleRentalStartSerializer
    permission_classes = [NoBicycle, permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Получаем данные из запроса
        bicycle_pk = self.request.data['bicycle']
        bicycle = Bicycle.objects.get(pk=bicycle_pk)
        user = User.objects.get(pk=self.request.user.pk)

        # Проверяем, не арендован ли уже выбранный велосипед
        if bicycle.rental_bicycle:
            raise serializers.ValidationError("This bicycle is already rented out.")

        # Устанавливаем флаг аренды для велосипеда
        bicycle.rental_bicycle = True
        bicycle.save()

        # Сохраняем аренду
        rental = serializer.save(user=user, bicycle=bicycle)
        rental.save()

    def get(self, request, *args, **kwargs):
        # Возвращает список доступных для аренды велосипедов
        free_bicycles = Bicycle.objects.filter(rental_bicycle=False)
        serializer = BicycleListSerializer(free_bicycles, many=True)
        return Response({'free_bicycle': serializer.data})


class ReturnBicycleView(generics.UpdateAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.datetime_rented_stop:
            return Response({"detail": "This rental has already been returned."}, status=status.HTTP_400_BAD_REQUEST)

        instance.datetime_rented_stop = timezone.now()

        instance.bicycle.rental_bicycle = False
        instance.bicycle.save()

        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
