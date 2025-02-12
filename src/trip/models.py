from django.db import models

from authentication.models import CustomUser


class State(models.Model):
    """
    Attributes:
        - name (CharField): The name of the state.
        - abbreviation (CharField): The abbreviation of the state.
        - country (CharField): The country of the state.

    Attributes inherits from Model:
        - id (AutoField): The primary key for the state.

    Methods:
        - save: Capitalizes the name and country of the state before saving it.
        - __str__: Returns a string representation of the state.

    Meta:
        - unique_together: The name, abbreviation and country of the state must be unique together.
    """

    name = models.CharField(max_length=100, verbose_name="Nombre")
    abbreviation = models.CharField(max_length=2, verbose_name="Abreviatura")
    country = models.CharField(max_length=100, verbose_name="País")

    def __str__(self):
        return f"{self.name}, {self.country}"

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        self.country = self.country.title()
        self.abbreviation = self.abbreviation.upper()

        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ("name", "abbreviation", "country")


class City(models.Model):
    """
    Attributes:
        - name (CharField): The name of the city.
        - latitude (FloatField): The latitude of the city.
        - longitude (FloatField): The longitude of the city.
        - state (CharField): The state of the city.

    Attributes inherits from Model:
        - id (AutoField): The primary key for the city.

    Methods:
        - save: Capitalizes the name of the city before saving it.
        - __str__: Returns a string representation of the city.
    """

    name = models.CharField(max_length=100, verbose_name="Nombre")
    latitude = models.FloatField(verbose_name="Latitud")
    longitude = models.FloatField(verbose_name="Longitud")
    state = models.ForeignKey(
        State, related_name="cities", on_delete=models.CASCADE, verbose_name="Provincia"
    )

    def __str__(self):
        return f"{self.name}, {self.state}"

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        self.full_clean()
        super().save(*args, **kwargs)


class Vehicle(models.Model):
    """
    Attributes:
        - owner (ForeignKey): The owner of the vehicle.
        - license_plate (CharField): The license plate of the vehicle.
        - brand (CharField): The brand of the vehicle.
        - model (CharField): The model of the vehicle.

    Attributes inherits from Model:
        - id (AutoField): The primary key for the vehicle.

    Methods:
        - __str__: Returns a string representation of the vehicle.

    Meta:
        - unique_together: The license plate and owner of the vehicle must be unique together.
    """

    owner = models.ForeignKey(
        CustomUser,
        related_name="vehicles",
        on_delete=models.CASCADE,
        verbose_name="Propietario",
    )
    license_plate = models.CharField(max_length=7, verbose_name="Patente", unique=True)
    brand = models.CharField(max_length=50, verbose_name="Marca")
    model = models.CharField(max_length=50, verbose_name="Modelo")

    def __str__(self):
        return f"{self.brand} {self.model} {self.license_plate}"

    def save(self, *args, **kwargs):
        self.brand = self.brand.title()
        self.model = self.model.title()
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ("license_plate", "owner")


class Trip(models.Model):
    """
    Attributes:
        - origin_city (ForeignKey): The origin city of the trip.
        - destination_city (ForeignKey): The destination city of the trip.
        - departure_date (DateField): The departure date of the trip.
        - departure_time (TimeField): The departure time of the trip.
        - pet_allowed (BooleanField): Indicates if pets are allowed in the trip.
        - smoking_allowed (BooleanField): Indicates if smoking is allowed in the trip.
        - kids_allowed (BooleanField): Indicates if kids are allowed in the trip.
        - vehicle (ForeignKey): The vehicle of the trip.
        - participants (ManyToManyField): The participants of the trip.
        - creator (ForeignKey): The creator of the trip.

    Attributes inherits from Model:
        - id (AutoField): The primary key for the trip.

    Methods:
        - __str__: Returns a string representation of the trip.
    """

    origin_city = models.ForeignKey(
        City,
        related_name="trips_from",
        on_delete=models.CASCADE,
        verbose_name="Ciudad de origen",
    )
    destination_city = models.ForeignKey(
        City,
        related_name="trips_to",
        on_delete=models.CASCADE,
        verbose_name="Ciudad de destino",
    )
    departure_date = models.DateField(verbose_name="Fecha de salida")
    departure_time = models.TimeField(verbose_name="Hora de salida")
    pet_allowed = models.BooleanField(
        default=False, verbose_name="Se permiten mascotas"
    )
    smoking_allowed = models.BooleanField(
        default=False, verbose_name="Se permite fumar"
    )
    kids_allowed = models.BooleanField(default=False, verbose_name="Se permiten niños")
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.SET_NULL, null=True, verbose_name="Vehículo"
    )
    participants = models.ManyToManyField(
        CustomUser,
        related_name="trips",
        through="TripParticipant",
        verbose_name="Participantes",
    )
    creator = models.ForeignKey(
        CustomUser,
        related_name="created_trips",
        on_delete=models.CASCADE,
        verbose_name="Creador",
    )

    def __str__(self):
        return f"from {self.origin_city} to {self.destination_city} on {self.departure_date}"


class TripParticipant(models.Model):
    """
    Attributes:
        - user (ForeignKey): The user of the trip.
        - trip (ForeignKey): The trip.
        - role (CharField): The role of the user on the trip.

    Attributes inherits from Model:
        - id (AutoField): The primary key for the participant.

    Methods:
        - __str__: Returns a string representation of the participant.

    Meta:
        - unique_together: The user and trip of the model must be unique together.
    """

    user = models.ForeignKey(
        CustomUser,
        related_name="user_trips",
        on_delete=models.CASCADE,
        verbose_name="Usuario",
    )
    trip = models.ForeignKey(
        Trip,
        related_name="trip_participants",
        on_delete=models.CASCADE,
        verbose_name="Viaje",
    )
    role = models.CharField(
        max_length=10,
        choices=[
            ("driver", "Driver"),
            ("passenger", "Passenger"),
        ],
        verbose_name="Rol",
    )

    def __str__(self):
        return f"{self.user.email} as {self.role} in trip {self.trip}"

    class Meta:
        unique_together = ("user", "trip")


class TripJoinRequest(models.Model):
    """
    Attributes:
        - user (ForeignKey): The user of the request.
        - trip (ForeignKey): The trip of the request.
        - created_at (DateTimeField): The creation date of the request.
        - updated_at (DateTimeField): The update date of the request.
        - status (CharField): The status of the request.

    Attributes inherits from Model:
        - id (AutoField): The primary key for the request.

    Methods:
        - __str__: Returns a string representation of the request.

    Meta:
        - unique_together: The user and trip of the request must be unique together.
    """

    user = models.ForeignKey(
        CustomUser,
        related_name="join_requests",
        on_delete=models.CASCADE,
        verbose_name="Usuario",
    )
    trip = models.ForeignKey(
        Trip,
        related_name="join_requests",
        on_delete=models.CASCADE,
        verbose_name="Viaje",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de actualización"
    )
    status = models.CharField(
        max_length=10,
        choices=[
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ],
        verbose_name="Estado",
        default="pending",
    )

    def __str__(self):
        return f"{self.user.email} request to join trip {self.trip}"

    class Meta:
        unique_together = ("user", "trip")
