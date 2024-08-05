from rest_framework import viewsets

from core.models import Airplane
from core.models import AirplaneType
from core.models import Airport
from core.models import City
from core.models import Country
from core.models import Crew
from core.models import Flight
from core.models import Order
from core.models import Route
from core.models import Ticket
from core.serializers import AirplaneSerializer
from core.serializers import AirplaneTypeSerializer
from core.serializers import AirportSerializer
from core.serializers import CitySerializer
from core.serializers import CountrySerializer
from core.serializers import CrewSerializer
from core.serializers import FlightSerializer
from core.serializers import OrderSerializer
from core.serializers import RouteSerializer
from core.serializers import TicketSerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class AirplaneTypesViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
