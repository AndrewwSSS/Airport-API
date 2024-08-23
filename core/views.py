from django.db.models import Count
from django.db.models import F
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from rest_framework.permissions import IsAdminUser

from core.filtersets import FlightFilterset
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
    FlightAdminDetailSerializer,
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
from core.serializers import FlightUserDetailSerializer


class GenericMethodsMapping:
    def get_serializer_class(self):
        if hasattr(self, "serializer_class_mapping"):
            return self.serializer_class_mapping.get(self.action, self.serializer_class)
        return self.serializer_class


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["name"]
    search_fields = ["name"]


class CityViewSet(GenericMethodsMapping, viewsets.ModelViewSet):
    queryset = City.objects.select_related("country")
    serializer_class = CitySerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = [
        "name",
        "country__name",
    ]
    search_fields = ["name"]
    serializer_class_mapping = {
        "retrieve": CityDetailSerializer,
        "list": CityListSerializer,
    }


class AirportViewSet(GenericMethodsMapping, viewsets.ModelViewSet):
    queryset = Airport.objects.select_related("closest_big_city")
    serializer_class = AirportSerializer
    permission_classes = [
        IsAdminOrAuthenticatedReadOnly,
    ]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["closest_big_city__name", "name"]
    search_fields = ["closest_big_city__name", "name"]
    serializer_class_mapping = {
        "retrieve": AirportDetailSerializer,
        "list": AirportListSerializer,
    }


class RouteViewSet(GenericMethodsMapping, viewsets.ModelViewSet):
    queryset = Route.objects.select_related("source", "destination")
    serializer_class = RouteSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["source__name", "destination__name"]
    serializer_class_mapping = {
        "retrieve": RouteDetailSerializer,
        "list": RouteListSerializer,
    }


class AirplaneTypesViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["name"]
    search_fields = ["name"]


class AirplaneViewSet(GenericMethodsMapping, viewsets.ModelViewSet):
    queryset = Airplane.objects.select_related("airplane_type")
    serializer_class = AirplaneSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["name"]
    search_fields = ["name"]
    serializer_class_mapping = {
        "retrieve": AirplaneDetailSerializer,
        "list": AirplaneListSerializer,
    }


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.prefetch_related("tickets")
        if not self.request.user.is_staff:
            queryset.filter(user=self.request.user)
        return queryset


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["first_name", "last_name"]
    search_fields = ["first_name", "last_name"]


class FlightViewSet(viewsets.ModelViewSet):
    serializer_class = FlightSerializer
    permission_classes = [
        IsAdminOrAuthenticatedReadOnly,
    ]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_class = FlightFilterset
    ordering_fields = [
        "airplane__name",
        "departure_time",
        "arrival_time",
        "route__source__name",
        "route__destination__name",
    ]
    search_fields = [
        "airplane__name",
        "route__name",
    ]

    def get_queryset(self):
        queryset = (
            Flight.objects.select_related(
                "airplane", "route__source", "route__destination"
            )
            .prefetch_related("crew")
            .annotate(
                tickets_available=F("airplane__rows") * F("airplane__seats_in_row")
                - Count("tickets"),
            )
        )
        if not self.request.user.is_staff:
            now = timezone.now()
            queryset = queryset.filter(departure_time__gt=now)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        elif self.action == "retrieve" and self.request.user.is_staff:
            return FlightAdminDetailSerializer
        elif self.action == "retrieve":
            return FlightUserDetailSerializer
        else:
            return self.serializer_class

    @vary_on_headers("Authorization")
    @method_decorator(cache_page(60 * 5, key_prefix="flights"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class TicketViewSet(GenericMethodsMapping, viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [
        IsAdminOrAuthenticatedReadOnly,
    ]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["flight__route__name"]
    search_fields = ["flight__route__name"]
    serializer_class_mapping = {
        "retrieve": TicketDetailSerializer,
        "list": TicketListSerializer,
    }

    def get_queryset(self):
        queryset = Ticket.objects.select_related(
            "flight__route__destination",
            "flight__route__source",
            "flight__airplane",
        )
        if not self.request.user.is_staff:
            queryset.filter(order__user=self.request.user)
        return queryset
