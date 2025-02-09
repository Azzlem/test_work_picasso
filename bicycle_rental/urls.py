from django.urls import path

from bicycle_rental.apps import BicycleRentalConfig
from bicycle_rental.views import ReturnBicycleView, BicycleRentalView, HistoryRentalView

app_name = BicycleRentalConfig.name

urlpatterns = [

    path('bicycle/rentals/return/', ReturnBicycleView.as_view(), name='bicycle-rental-stop'),

    path('bicycle/rental/', BicycleRentalView.as_view(), name='bicycle-rental-start'),

    path('bicycle/history/', HistoryRentalView.as_view(), name='bicycle-rental-history')
]
