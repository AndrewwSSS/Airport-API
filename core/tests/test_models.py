from django.test import TestCase

from core.models import Airplane
from core.models import AirplaneType
from core.models import Airport
from core.models import City
from core.models import Country
from core.models import Crew
from core.models import Route


class CountryModelTest(TestCase):
    def setUp(self):
        self.country_name = "Ukraine"
        self.country = Country.objects.create(
            name=self.country_name,
        )

    def test_country_str(self):
        self.assertEqual(str(self.country), self.country_name)


class CityModelTest(TestCase):
    def setUp(self):
        self.city_name = "Mykolaiv"
        self.country_name = "Ukraine"
        self.country = Country.objects.create(
            name=self.country_name,
        )
        self.city = City.objects.create(
            name=self.city_name,
            country=self.country,
        )

    def test_city_str(self):
        self.assertEqual(str(self.city), f"{self.city_name} ({self.country_name})")


class AirportModelTest(TestCase):
    def setUp(self):
        self.city_name = "Mykolaiv"
        self.country_name = "Ukraine"
        self.airport_name = "Mykolaiv International Airport"
        self.country = Country.objects.create(
            name=self.country_name,
        )
        self.city = City.objects.create(
            name=self.city_name,
            country=self.country,
        )
        self.airport = Airport.objects.create(
            name=self.airport_name,
            closest_big_city=self.city,
        )

    def test_airport_str(self):
        self.assertEqual(str(self.airport), self.airport_name)


class RouteModelTest(TestCase):
    def setUp(self):
        self.city_name_1 = "Mykolaiv"
        self.city_name_2 = "Kiev"
        self.country_name = "Ukraine"
        self.airport_name_1 = "Mykolaiv International Airport"
        self.airport_name_2 = "Borispil International Airport"
        self.country = Country.objects.create(
            name=self.country_name,
        )
        self.city_1 = City.objects.create(
            name=self.city_name_1,
            country=self.country,
        )
        self.city_2 = City.objects.create(
            name=self.city_name_2,
            country=self.country,
        )

        self.airport_1 = Airport.objects.create(
            name=self.airport_name_1,
            closest_big_city=self.city_1,
        )
        self.airport_2 = Airport.objects.create(
            name=self.airport_name_1, closest_big_city=self.city_2
        )
        self.route = Route.objects.create(
            source=self.airport_1, destination=self.airport_2, distance=500
        )

    def test_route_str(self):
        self.assertEqual(
            str(self.route), f"{self.airport_1.name} - {self.airport_2.name}"
        )

    def test_route_name(self):
        self.assertEqual(
            self.route.name, f"{self.airport_1.name} - {self.airport_2.name}"
        )


class AirplaneTypeModelTest(TestCase):
    def setUp(self):
        self.airplane_type_name = "Jumbo Jet"
        self.airplane_type = AirplaneType.objects.create(
            name=self.airplane_type_name,
        )

    def test_airplane_type_str(self):
        self.assertEqual(str(self.airplane_type), self.airplane_type_name)


class AirplaneModelTest(TestCase):
    def setUp(self):
        self.airplane_type_name = "Jumbo Jet"
        self.airplane_name = "Boing 777"
        self.airplane_type = AirplaneType.objects.create(
            name=self.airplane_type_name,
        )
        self.airplane = Airplane.objects.create(
            airplane_type=self.airplane_type,
            name=self.airplane_name,
            seats_in_row=4,
            rows=50,
        )

    def test_airplane_str(self):
        self.assertEqual(str(self.airplane), self.airplane_name)


class CrewModelTest(TestCase):
    def setUp(self):
        self.first_name = "Aboba"
        self.last_name = "Yahontov"
        self.crew = Crew.objects.create(
            first_name=self.first_name, last_name=self.last_name
        )

    def test_crew_str(self):
        self.assertEqual(
            str(self.crew),
            f"{self.first_name} {self.last_name}",
        )

    def test_crew_full_name(self):
        self.assertEqual(
            str(self.crew),
            f"{self.first_name} {self.last_name}",
        )
