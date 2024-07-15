import pytest

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from bicycle_rental.models import Bicycle, Rental
from users.models import User


def user_bild():
    return User.objects.create_user(
        email='test@test.text',
        password='<PASSWORD>',
        name='Test User',
    )


def bicycle_bild():
    return Bicycle.objects.create(
        name='Test Bicycle',
    )


def api_client_bild():
    return APIClient()


def authenticated_client_build(api_client):
    user = user_bild()
    api_client.force_authenticate(user=user)
    return api_client, user


@pytest.mark.django_db
def test_rent_bicycle():
    bicycle = bicycle_bild()
    authenticated_client, user = authenticated_client_build(api_client_bild())
    url = reverse('bicycle_rental:bicycle-rental-start')
    response = authenticated_client.post(url, {'bicycle': bicycle.id}, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['bicycle'] == bicycle.id
    assert response.data['user'] == authenticated_client.handler._force_user.id


@pytest.mark.django_db
def test_return_bicycle():
    authenticated_client, user = authenticated_client_build(api_client_bild())
    bicycle = bicycle_bild()  # Ваша функция для создания велосипеда
    rental = Rental.objects.create(user=user, bicycle=bicycle)
    url = reverse('bicycle_rental:bicycle-rental-stop')
    response = authenticated_client.patch(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    rental.refresh_from_db()
    assert rental.datetime_rented_stop is not None


@pytest.mark.django_db
def test_rental_history():
    authenticated_client, user = authenticated_client_build(api_client_bild())
    bicycle = bicycle_bild()
    rental1 = Rental.objects.create(user=user, bicycle=bicycle)
    rental2 = Rental.objects.create(user=user, bicycle=bicycle, datetime_rented_stop=timezone.now())
    url = reverse('bicycle_rental:bicycle-rental-history')
    response = authenticated_client.get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['rental_history']) == 2
