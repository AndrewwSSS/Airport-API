from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from core.models import (
    Airplane,
    AirplaneType,
    Airport,
    City,
    Country,
    Crew,
    Flight,
    Order,
    Route,
    Ticket,
)
from core.permissions import IsAdminOrAuthenticatedReadOnly
from core.serializers import (
    AirplaneDetailSerializer,
    AirplaneListSerializer,
    AirplaneSerializer,
    AirplaneTypeSerializer,
    AirportDetailSerializer,
    AirportListSerializer,
    AirportSerializer,
    CityDetailSerializer,
    CityListSerializer,
    CitySerializer,
    CountrySerializer,
    CrewSerializer,
    FlightDetailSerializer,
    FlightListSerializer,
    FlightSerializer,
    OrderSerializer,
    RouteDetailSerializer,
    RouteListSerializer,
    RouteSerializer,
    TicketDetailSerializer,
    TicketListSerializer,
    TicketSerializer,
)


class GenericMethodsMapping:
    def get_serializer_class(self):
        if hasattr(self, "serializer_class_mapping"):
            return self.serializer_class_mapping.get(
                self.action,
                self.serializer_class
            )
        return self.serializer_class


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAdminOrAuthenticatedReadOnly,]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["name"]
    search_fields = ["name"]


class CityViewSet(GenericMethodsMapping, viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAdminOrAuthenticatedReadOnly,]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["name"]
    search_fields = ["name"]
    serializer_class_mapping = {
        "retrieve": CityDetailSerializer,
        "list": CityListSerializer,
    }


class AirportViewSet(GenericMethodsMapping, viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsAdminOrAuthenticatedReadOnly,]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["closest_big_city__name", "name"]
    search_fields = ["closest_big_city__name", "name"]
    serializer_class_mapping = {
        "retrieve": AirportDetailSerializer,
        "list": AirportListSerializer,
    }


class RouteViewSet(GenericMethodsMapping, viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [IsAdminOrAuthenticatedReadOnly,]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["source__name", "destination__name"]
    serializer_class_mapping = {
        "retrieve": RouteDetailSerializer,
        "list": RouteListSerializer
    }


class AirplaneTypesViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = [IsAdminOrAuthenticatedReadOnly,]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["name"]
    search_fields = ["name"]


class AirplaneViewSet(GenericMethodsMapping, viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = [IsAdminOrAuthenticatedReadOnly,]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["name"]
    search_fields = ["name"]
    serializer_class_mapping = {
        "retrieve": AirplaneDetailSerializer,
        "list": AirplaneListSerializer
    }


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.all()
        if not self.request.user.is_staff:
            queryset.filter(user=self.request.user)
        return queryset


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = [IsAdminOrAuthenticatedReadOnly,]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["first_name", "last_name"]
    search_fields = ["first_name", "last_name"]


class FlightViewSet(GenericMethodsMapping, viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [IsAdminOrAuthenticatedReadOnly,]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = [
        "airplane",
        "departure_time",
        "arrival_time",
        "route__source__name",
        "route__destination__name",
    ]
    search_fields = [
        "airplane__name",
        "departure_time",
        "arrival_time",
        "route__name"
    ]
    serializer_class_mapping = {
        "retrieve": FlightDetailSerializer,
        "list": FlightListSerializer,
    }


class TicketViewSet(GenericMethodsMapping, viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAdminOrAuthenticatedReadOnly,]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["flight__route__name"]
    search_fields = ["flight__route__name"]
    serializer_class_mapping = {
        "retrieve": TicketDetailSerializer,
        "list": TicketListSerializer,
    }

    def get_queryset(self):
        queryset = Ticket.objects.all()
        if not self.request.user.is_staff:
            queryset.filter(order__user=self.request.user)
        return queryset
