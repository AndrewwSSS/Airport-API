from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = [
            "id",
            "name"
        ]


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = [
            "id",
            "name",
            "country"
        ]


class CityListSerializer(CitySerializer):
    country = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="name"
    )


class CityDetailSerializer(CitySerializer):
    country = CountrySerializer()


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = [
            "id",
            "name",
            "closest_big_city"
        ]


class AirportListSerializer(AirportSerializer):
    closest_big_city = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="name"
    )


class AirportDetailSerializer(AirportSerializer):
    closest_big_city = CityDetailSerializer(many=False)


class RouteSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        source = attrs.get("source")
        destination = attrs.get("destination")
        if not source or not destination:
            return attrs
        Route.validate_source_and_destination(
            source,
            destination,
            ValidationError
        )
        return attrs

    class Meta:
        model = Route
        fields = [
            "id",
            "source",
            "destination",
            "distance"
        ]


class RouteListSerializer(RouteSerializer):
    source = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="name"
    )
    destination = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="name"
    )


class RouteDetailSerializer(RouteSerializer):
    source = AirportDetailSerializer(many=False)
    destination = AirportDetailSerializer(many=False)


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = [
            "id",
            "name"
        ]


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "id",
            "row",
            "seat",
            "order",
            "flight"
        ]


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = [
            "id",
            "name",
            "rows",
            "seats_in_row",
            "airplane_type",
        ]


class AirplaneListSerializer(AirplaneSerializer):
    airplane_type = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="name"
    )


class AirplaneDetailSerializer(AirplaneSerializer):
    airplane_type = AirplaneTypeSerializer(many=False)


class FlightSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        departure_time = attrs.get("departure_time")
        arrival_time = attrs.get("arrival_time")
        airplane = attrs.get("airplane")
        if not departure_time or not arrival_time:
            return attrs
        Flight.validate_departure_time_and_arrival_time(
            departure_time,
            arrival_time,
            ValidationError
        )
        flights = Flight.objects.filter(
            airplane=airplane,
            departure_time__gte=departure_time,
            arrival_time__lte=arrival_time
        )
        if flights.exists():
            raise ValidationError(
                {
                    "airplane": "This airplane has flight in this time."
                }
            )
        return attrs

    class Meta:
        model = Flight
        fields = [
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
        ]


class FlightListSerializer(FlightSerializer):
    airplane = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="name"
    )
    route = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="name"
    )


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = [
            "id",
            "first_name",
            "last_name",
        ]


class FlightDetailSerializer(FlightSerializer):
    airplane = AirplaneDetailSerializer(many=False)
    crew = CrewSerializer(many=True)
    route = RouteDetailSerializer(many=False)

    class Meta:
        model = Flight
        fields = FlightSerializer.Meta.fields + [
            "crew"
        ]


class TicketCreateWithOrderSerializer(TicketSerializer):
    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["flight"],
            ValidationError
        )
        return data

    class Meta:
        model = Ticket
        fields = [
            "id",
            "row",
            "seat",
            "flight"
        ]


class TicketDetailSerializer(TicketSerializer):
    flight = FlightDetailSerializer(many=False)

    class Meta:
        model = Ticket
        fields = [
            "id",
            "row",
            "seat",
            "flight"
        ]


class TicketListSerializer(TicketSerializer):
    flight = FlightListSerializer(many=False)


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketCreateWithOrderSerializer(many=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "tickets",
            "created_at"
        ]

    def create(self, validated_data):
        tickets = validated_data.pop("tickets")
        order = Order.objects.create(
            **validated_data,
            user=self.context["request"].user
        )
        for ticket in tickets:
            ticket = Ticket(**ticket)
            ticket.order = order
            ticket.save()
        return order


class OrderDetailSerializer(serializers.ModelSerializer):
    tickets = TicketDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "tickets",
            "created_at"
        ]
