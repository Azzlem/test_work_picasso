from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, serializers, status

from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.views import APIView

from bicycle_rental.models import Bicycle, Rental
from bicycle_rental.permissions import NoBicycle
from bicycle_rental.serializers import BicycleListSerializer, BicycleRentalStartSerializer, RentalSerializer

from .tasks import calculate_rental_cost


class BicycleRentalView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get available bicycles for rental",
        responses={200: BicycleListSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        free_bicycles = Bicycle.objects.filter(rental_bicycle=False)
        serializer = BicycleListSerializer(free_bicycles, many=True)
        return Response({'free_bicycles': serializer.data})

    @swagger_auto_schema(
        operation_description="Rent a bicycle",
        request_body=BicycleRentalStartSerializer,
        responses={201: BicycleRentalStartSerializer,
                   403: 'You cannot rent another bicycle while having an active rental.'}
    )
    def post(self, request, *args, **kwargs):
        permission = NoBicycle()
        if not permission.has_permission(request, self):
            return Response({"detail": "You cannot rent another bicycle while having an active rental."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = BicycleRentalStartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bicycle = serializer.validated_data['bicycle']
        user = request.user

        if bicycle.rental_bicycle:
            raise serializers.ValidationError("This bicycle is already rented out.")

        bicycle.rental_bicycle = True
        bicycle.save()

        rental = serializer.save(user=user, bicycle=bicycle)
        rental.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReturnBicycleView(generics.UpdateAPIView):
    serializer_class = RentalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Rental.objects.all()

    def put(self, request, *args, **kwargs):
        try:
            rental = Rental.objects.get(user=request.user, datetime_rented_stop=None)
        except Rental.DoesNotExist:
            return Response({"detail": "No active rental found for this user."}, status=status.HTTP_404_NOT_FOUND)

        rental.datetime_rented_stop = timezone.now()
        rental.bicycle.rental_bicycle = False
        rental.bicycle.save()
        rental.save()

        calculate_rental_cost.delay(rental.id)

        serializer = RentalSerializer(rental)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        try:
            rental = Rental.objects.get(user=request.user, datetime_rented_stop=None)
        except Rental.DoesNotExist:
            return Response({"detail": "No active rental found for this user."}, status=status.HTTP_404_NOT_FOUND)

        rental.datetime_rented_stop = timezone.now()
        rental.bicycle.rental_bicycle = False
        rental.bicycle.save()
        rental.save()

        calculate_rental_cost.delay(rental.id)

        serializer = RentalSerializer(rental)
        return Response(serializer.data)


class HistoryRentalView(generics.ListAPIView):
    serializer_class = RentalSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        rental_history = Rental.objects.filter(user=self.request.user)
        serializer = RentalSerializer(rental_history, many=True)
        return Response({'rental_history': serializer.data})
