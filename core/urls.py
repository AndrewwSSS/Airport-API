from django.urls import include, path
from rest_framework import routers

from core.views import (
    AirplaneTypesViewSet,
    AirplaneViewSet,
    AirportViewSet,
    CityViewSet,
    CountryViewSet,
    CrewViewSet,
    FlightViewSet,
    OrderViewSet,
    RouteViewSet,
    TicketViewSet,
)

router = routers.DefaultRouter()
router.register("countries", CountryViewSet)
router.register("cities", CityViewSet)
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)
router.register("airplane-types", AirplaneTypesViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("orders", OrderViewSet, basename="orders")
router.register("crews", CrewViewSet)
router.register("flights", FlightViewSet, basename="flights")
router.register("tickets", TicketViewSet, basename="tickets")

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "core"
