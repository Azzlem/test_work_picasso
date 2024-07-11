from django.urls import path

from bicycle_rental.apps import BicycleRentalConfig
from bicycle_rental.views import BicycleListView, BicycleStartRentalView, ReturnBicycleView

app_name = BicycleRentalConfig.name

urlpatterns = [
    path('bicycles', BicycleListView.as_view(), name='list_free_bicycle'),
    path('start-rental', BicycleStartRentalView.as_view(), name='start_rental'),
    path('stop-rental/<int:pk>/', ReturnBicycleView.as_view(), name='stop-rental'),
]
