from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from django.utils import timezone


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="cities",
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["name", "country"],
                name="unique_city_for_country",
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.country})"


class Airport(models.Model):
    name = models.CharField(max_length=100)
    closest_big_city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="airports",
    )

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="source_routes",
    )
    destination = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="destination_routes",
    )
    distance = models.IntegerField(
        validators=[
            MinValueValidator(10)
        ]
    )

    @staticmethod
    def validate_source_and_destination(source, destination, exception) -> None:
        if source == destination:
            raise exception(
                {
                    "source": "Source and destination must be different"
                }
            )
        queryset = Route.objects.filter(source=source, destination=destination)
        if queryset.exists():
            raise exception(
                {
                    "__all__": "This rout already exists"
                }
            )

    def validate(self):
        self.validate_source_and_destination(
            self.source,
            self.destination,
            ValidationError
        )

    def __str__(self):
        return f"{self.source.name} - {self.destination.name}"

    @property
    def name(self):
        return str(self)


class AirplaneType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField(
        validators=[
            MinValueValidator(3),
            MaxValueValidator(5),
        ]
    )
    seats_in_row = models.IntegerField(
        validators=[
            MinValueValidator(2),
            MaxValueValidator(100),
        ]
    )
    airplane_type = models.ForeignKey(
        AirplaneType,
        on_delete=models.CASCADE,
        related_name="airplanes",
    )

    def __str__(self):
        return self.name


class Crew(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self) -> str:
        return str(self)


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
    )

    def __str__(self):
        return f"{self.created_at} - {self.user}"


class Flight(models.Model):
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="flights",
    )
    airplane = models.ForeignKey(
        Airplane,
        on_delete=models.CASCADE,
        related_name="flights",
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew)

    @staticmethod
    def validate_departure_time_and_arrival_time(
            departure_time,
            arrival_time,
            exception
    ):
        if departure_time <= timezone.now():
            raise exception(
                {
                    "departure_time": "departure_time must be less than now"
                }
            )
        if departure_time >= arrival_time:
            raise exception(
                {
                    "departure_time": "Departure time is greater than arrival time"
                }
            )

    def validate(self):
        self.validate_departure_time_and_arrival_time(
            self.departure_time,
            self.arrival_time,
            ValidationError
        )

    def __str__(self):
        return f"{self.route} / {self.departure_time} - {self.arrival_time}"


class Ticket(models.Model):
    row = models.IntegerField(
        validators=[
            MinValueValidator(1),
        ]
    )
    seat = models.IntegerField(
        validators=[
            MinValueValidator(1),
        ]
    )
    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name="tickets",
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tickets",
    )


    @staticmethod
    def validate_ticket(
            row: int,
            seat: int,
            flight: Flight,
            error,
    ) -> None:
        if row > flight.airplane.rows:
            raise error(
                {
                    "row": "Invalid row"
                }
            )
        if seat > flight.airplane.seats_in_row:
            raise error(
                {
                    "seat": "Invalid seat"
                }
            )
        queryset = flight.tickets.filter(
            seat=seat,
            row=row
        )
        if queryset.exists():
            raise error(
                {
                    "seat": "Ticket already exists"
                }
            )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["flight", "row", "seat"],
                name="unique_tickets_for_flight",
            )
        ]

    def __str__(self):
        return f"row: {self.row} / seat: {self.seat}"
