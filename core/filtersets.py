from django_filters import rest_framework as filters

from core.models import Flight


class FlightFilterset(filters.FilterSet):
    departure_time_from = filters.DateTimeFilter(
        field_name="departure_time",
        lookup_expr="gte",
    )
    arrival_time_from = filters.DateTimeFilter(
        field_name="arrival_time",
        lookup_expr="gte",
    )
    departure_time_to = filters.DateTimeFilter(
        field_name="departure_time",
        lookup_expr="lte",
    )
    arrival_time_to = filters.DateTimeFilter(
        field_name="arrival_time",
        lookup_expr="lte",
    )

    class Meta:
        model = Flight
        fields = [
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
        ]
