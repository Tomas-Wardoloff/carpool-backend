import re
from datetime import datetime, timedelta
from rest_framework import serializers

from authentication.models import CustomUser
from .models import State, City, Vehicle, Trip, TripParticipant, TripJoinRequest


class StateSerializer(serializers.ModelSerializer):
    """
    This serializer handles the serialization of State instances.
    Excluded fields: 'country'.
    """

    class Meta:
        model = State
        fields = ["id", "name", "abbreviation"]
        read_only_fields = ["id", "name", "abbreviation"]


class CitySerializer(serializers.ModelSerializer):
    """
    This serializer handles the serialization of City instances.
    No excluded fields.
    """

    state = StateSerializer()

    class Meta:
        model = City
        fields = ["id", "name", "latitude", "longitude", "state"]
        read_only_fields = ["id", "name", "latitude", "longitude", "state"]


class VehicleDetailSerializer(serializers.ModelSerializer):
    """
    This serializer handles the serialization and deserialization of Vehicle instances
    for the create, retrieve and update actions, ensuring that all necessary fields are included.
    Excluded fields: 'owner'.

    Methods:
        validate_license_plate():
            Validates the license plate format.
        validate():
            Validates that the user does not have a vehicle with the same license plate before saving.
    """

    class Meta:
        model = Vehicle
        fields = ["id", "license_plate", "brand", "model"]
        read_only_fields = ["id"]

    def validate_license_plate(self, value):
        if not re.match(r"^(?:[A-Z]{3}\d{3}|[A-Z]{2}\d{3}[A-Z]{2})$", value):
            raise serializers.ValidationError(
                "Patente invalida"
            )  # check license plate FORMAT: ABC123 or AB123CD
        return value

    def validate(self, data):
        license_plate = data.get("license_plate")
        owner = self.context["request"].user

        if Vehicle.objects.filter(owner=owner, license_plate=license_plate).exists():
            raise serializers.ValidationError(
                "El usuario ya cuenta con un vehículo registrado con esa patente"
            )  # check if the user already has a vehicle with the same license plate before save
        return data


class VehicleListSerializer(serializers.ModelSerializer):
    """
    This serializer handles the serialization of Vehicle instances for the list action,
    including only the 'id', 'brand', and 'model' fields to avoid exposing sensitive data.
    """

    class Meta:
        model = Vehicle
        fields = ["id", "brand", "model"]
        read_only_fields = ["id", "brand", "model"]


class TripParticipantDetailSerializer(serializers.ModelSerializer):
    """
    This serializer handles the serialization and deserialization of TripParticipant instances
    for the create, retrieve and update actions.
    Excluded fields: 'user'.

    Methods:
        validate_trip():
            Validates that the trip exists.
        validate_role():
            Validates that the role is either 'passanger' or 'driver'.
    """

    trip = serializers.PrimaryKeyRelatedField(queryset=Trip.objects.all())

    class Meta:
        model = TripParticipant
        fields = ["id", "trip", "role"]
        read_only_fields = ["id"]

    def validate_trip(self, value):
        if not Trip.objects.filter(id=value).exists():
            raise serializers.ValidationError("El viaje especificado no existe")
        return value

    def validate_role(self, value):
        if value not in ("passanger", "driver"):
            raise serializers.ValidationError("El rol especificado es invalido")
        return value


class TripParticipantListSerializer(serializers.ModelSerializer):
    """
    This serializer handles the serialization of TripParticipant instances for the list action,
    including fields that provide an overview of the participant's involvement in the trip.
    """

    user = serializers.SlugRelatedField(
        slug_field="first_name", queryset=CustomUser.objects.all()
    )
    trip = serializers.PrimaryKeyRelatedField(queryset=Trip.objects.all())

    class Meta:
        model = TripParticipant
        fields = ["id", "user", "role", "trip"]
        read_only_fields = ["id", "user", "role", "trip"]


class TripDetailSerializer(serializers.ModelSerializer):
    """
    Serializer class for creating and updating Trip instances.

    This serializer handles the serialization and deserialization of Trip instances
    for the create, retrieve and update actions.
    """

    origin_city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    destination_city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    vehicle = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all())

    class Meta:
        model = Trip
        fields = [
            "id",
            "origin_city",
            "destination_city",
            "departure_time",
            "pet_allowed",
            "smoking_allowed",
            "kids_allowed",
            "vehicle",
        ]
        read_only_fields = ["id"]

    def validate_departure_date(self, value):
        one_year_from_now = datetime.now().date() + timedelta(days=365)
        if value > one_year_from_now:
            raise serializers.ValidationError(
                "La fecha de salida no puede ser superior a un año desde la fecha actual"
            )
        return value

    def validate(self, data):
        departure_date = data.get("departure_date")
        departure_time = data.get("departure_time")

        if data.get("origin_city") == data.get("destination_city"):
            raise serializers.ValidationError(
                "La ciudad de origen y de destino no puede ser la misma ciudad"
            )
        if datetime.combine(departure_date, departure_time) < datetime.now():
            raise serializers.ValidationError(
                "La fecha de salida no puede ser anterior a la fecha actual"
            )
        return data


class TripListSerializer(serializers.ModelSerializer):
    """
    This serializer handles the serialization of Trip instances for the list action,
    including fields that provide an overview of the trip.
    """

    origin_city = serializers.StringRelatedField()
    destination_city = serializers.StringRelatedField()
    vehicle = VehicleListSerializer()
    participants = TripParticipantListSerializer(many=True)

    class Meta:
        model = Trip
        fields = [
            "id",
            "origin_city",
            "destination_city",
            "departure_date",
            "departure_time",
            "pet_allowed",
            "smoking_allowed",
            "kids_allowed",
            "vehicle",
            "participants",
        ]
        read_only_fields = [
            "id",
            "origin_city",
            "detination_city",
            "departure_date",
            "departure_time",
            "pet_allowed",
            "smoking_allowed",
            "kids_allowed",
            "vehicle",
            "participants",
        ]


class TripJoinRequestSerializer(serializers.ModelSerializer):
    """
    Seriliazer class for creating and updating TripJoinRequest instances.
    """

    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    trip = serializers.PrimaryKeyRelatedField(queryset=Trip.objects.all())

    class Meta:
        model = TripJoinRequest
        fields = ["id", "user", "trip", "status"]
        read_only_fields = ["id"]

    def validate_status(self, value):
        if value not in ("pending", "accepted", "rejected"):
            raise serializers.ValidationError("El estado especificado es invalido")
        return value

    def validate(self, data):
        user = data.get("user")
        trip = data.get("trip")

        if TripJoinRequest.objects.filter(user=user, trip=trip).exists():
            raise serializers.ValidationError(
                "Ya existe una solicitud de unión para dicho viaje"
            )
        if trip.creator == user:
            raise serializers.ValidationError(
                "El creador del viaje no puede solicitar unirse a su propio viaje"
            )
        return data
