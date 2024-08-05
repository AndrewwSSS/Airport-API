from django.urls import include
from django.urls import path
from rest_framework import routers

from core.views import AirplaneTypesViewSet
from core.views import AirplaneViewSet
from core.views import AirportViewSet
from core.views import CityViewSet
from core.views import CountryViewSet
from core.views import CrewViewSet
from core.views import FlightViewSet
from core.views import OrderViewSet
from core.views import RouteViewSet
from core.views import TicketViewSet

router = routers.DefaultRouter()
router.register("countries", CountryViewSet)
router.register("cities", CityViewSet)
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)
router.register("airplane-types", AirplaneTypesViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("orders", OrderViewSet)
router.register("crews", CrewViewSet)
router.register("flights", FlightViewSet)
router.register("tickets", TicketViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "core"
