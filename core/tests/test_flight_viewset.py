import uuid
from random import randint

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Airplane
from core.models import AirplaneType
from core.models import Airport
from core.models import City
from core.models import Country
from core.models import Flight
from core.models import Route
from core.serializers import FlightListSerializer
from user.models import User


FLIGHTS_URL = "/api/airport/flights/"


def sample_user(**kwargs) -> User:
    data = {
        "username": "test",
        "password": "<PASSWORD>",
    }
    data.update(kwargs)
    return User.objects.create_user(**data)


def sample_city(**kwargs) -> City:
    data = {
        "name": str(uuid.uuid4()),
        "country": sample_country(),
    }
    data.update(kwargs)
    return City.objects.create(**data)


def sample_country(**kwargs) -> Country:
    data = {
        "name": str(uuid.uuid4()),
    }
    data.update(kwargs)
    return Country.objects.create(**data)


def sample_airplane_type(**kwargs) -> AirplaneType:
    data = {
        "name": str(uuid.uuid4()),
    }
    data.update(kwargs)
    return AirplaneType.objects.create(**data)


def sample_airplane(**kwargs) -> Airplane:
    data = {
        "name": str(uuid.uuid4()),
        "airplane_type": sample_airplane_type(),
        "rows": randint(20, 40),
        "seats_in_row": randint(1, 5),
    }
    data.update(kwargs)
    return Airplane.objects.create(**data)


def sample_flight(**kwargs) -> Flight:
    return Flight.objects.create(**kwargs)


def sample_airport(**kwargs) -> Airport:
    data = {
        "name": str(uuid.uuid4()),
        "closest_big_city": sample_city(),
    }
    data.update(kwargs)
    return Airport.objects.create(**data)


def sample_route(**kwargs) -> Route:
    data = {
        "source": sample_airport(),
        "destination": sample_airport(),
        "distance": randint(50, 600),
    }
    data.update(kwargs)
    return Route.objects.create(**data)


class FlightViewSetTest(TestCase):
    def setUp(self):
        self.route_1 = sample_route()
        self.route_2 = sample_route()
        self.airplane_1 = sample_airplane()
        self.airplane_2 = sample_airplane()

        self.flight_1 = Flight.objects.create(
            route=self.route_1,
            airplane=self.airplane_1,
            departure_time=timezone.now() + timezone.timedelta(days=1),
            arrival_time=timezone.now() + timezone.timedelta(days=1, hours=4),
        )
        self.flight_2 = Flight.objects.create(
            route=self.route_2,
            airplane=self.airplane_1,
            departure_time=timezone.now() + timezone.timedelta(days=2),
            arrival_time=timezone.now() + timezone.timedelta(days=2, hours=4),
        )
        self.flight_3 = Flight.objects.create(
            route=self.route_2,
            airplane=self.airplane_1,
            departure_time=timezone.now() - timezone.timedelta(days=3, hours=4),
            arrival_time=timezone.now() - timezone.timedelta(days=3),
        )
        self.client = APIClient()

        self.flight_1_serializer = FlightListSerializer(self.flight_1, many=False)
        self.flight_2_serializer = FlightListSerializer(self.flight_2, many=False)
        self.flight_3_serializer = FlightListSerializer(self.flight_3, many=False)

    def test_list_only_relevant_flights_for_user(self):
        user = sample_user()
        self.client.force_authenticate(user=user)
        response = self.client.get(FLIGHTS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for flight in response.data["results"]:
            flight.pop("tickets_available")

        results = response.data["results"]

        self.assertIn(
            self.flight_1_serializer.data,
            results,
        )
        self.assertIn(
            self.flight_2_serializer.data,
            results,
        )
        self.assertNotIn(self.flight_3_serializer.data, results)

    def test_list_all_flights_for_admin(self):
        user = sample_user(is_staff=True, username="admin")
        self.client.force_authenticate(user=user)
        response = self.client.get(FLIGHTS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for flight in response.data["results"]:
            flight.pop("tickets_available")

        results = response.data["results"]

        self.assertIn(
            self.flight_1_serializer.data,
            results,
        )
        self.assertIn(
            self.flight_2_serializer.data,
            results,
        )
        self.assertIn(self.flight_3_serializer.data, results)
