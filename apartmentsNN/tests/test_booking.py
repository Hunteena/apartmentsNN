from datetime import date, timedelta

import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient

from booking.models import Status, Booking, period
from flats.models import Apartment


BOOKING_EXAMPLE = {
    "name": "John Doe",
    "phone": "123456789",
    "email": "johndoe@example.com",
    "guests": {
        "adult": 1,
        "children": 0
    },
}


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def apartment_factory():
    def factory(*args, **kwargs):
        return baker.make(Apartment, *args, **kwargs)
    return factory


@pytest.fixture
def booking_factory():
    def factory(*args, **kwargs):
        return baker.make(Booking, *args, **kwargs)
    return factory


def today_plus_n_days(n: int) -> str:
    return str(date.today() + timedelta(days=n))


@pytest.mark.django_db
class TestBookingAPI:
    def test_create_booking(self, api_client, apartment_factory):
        # test simple creating
        apartment = apartment_factory()
        url = reverse('booking')
        booking = {
            "dateFrom": today_plus_n_days(0),
            "dateTo": today_plus_n_days(1),
            **BOOKING_EXAMPLE,
            "apartment": apartment.id,
        }

        response = api_client.post(url, booking)
        assert response.status_code == status.HTTP_201_CREATED, "Create"

        # test that last day of booking is free
        booking = {
            "dateFrom": today_plus_n_days(1),
            "dateTo": today_plus_n_days(5),
            **BOOKING_EXAMPLE,
            "apartment": apartment.id,
        }

        response = api_client.post(url, booking)
        assert response.status_code == status.HTTP_201_CREATED, "Last day of booking"

        # test creating booking with reserved dates
        response = api_client.post(url, booking)
        assert response.status_code == status.HTTP_400_BAD_REQUEST, "With reserved dates"

        # test creating with crossdates
        booking = {
            "dateFrom": today_plus_n_days(0),
            "dateTo": today_plus_n_days(10),
            **BOOKING_EXAMPLE,
            "apartment": apartment.id,
            "crossDates": True
        }

        response = api_client.post(url, booking)
        assert response.status_code == status.HTTP_201_CREATED, "With crossdates"
        assert response.data.get('status') == Status.pending, "Status pending"

    def test_reserved_dates(self, api_client, booking_factory):
        url = reverse('dates')
        start, end = date.today(), date.today() + timedelta(days=10)
        booking = booking_factory(
            dateFrom=start,
            dateTo=end,
            status=Status.confirmed
        )

        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK, "Get reserved dates"
        assert response.data[0]['dates'] == period(start, end), "Correct dates"
