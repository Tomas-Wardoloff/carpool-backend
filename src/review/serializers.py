from rest_framework import serializers

from .models import Review
from trip.models import Trip, TripParticipant
from authentication.models import CustomUser


class ReviewDetailSerializer(serializers.ModelSerializer):
    """
    This serializer handles the serialization of Review instances.
    Excluded fields: 'reviewer'.

    Methods:
        validate_rating():
            Validates that the rating is between 1 and 5.
        validate():
            Validates that the user and reviewer participated in the trip.
    """

    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    trip = serializers.PrimaryKeyRelatedField(queryset=Trip.objects.all())

    class Meta:
        model = Review
        fields = ["id", "user", "reviewer", "trip", "rating", "comment"]
        read_only_fields = ["id"]

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "La calificación debe ser un valor entre 1 y 5"
            )
        return value

    def validate(self, data):
        trip = data.get("trip")
        user = data.get("user")
        reviewer = data.get("reviewer")

        if not TripParticipant.objects.filter(user=user, trip=trip).exists():
            raise serializers.ValidationError(
                "El usuario especificado no participo en el viaje"
            )

        if not TripParticipant.objects.filter(user=reviewer, trip=trip).exists():
            raise serializers.ValidationError(
                "El revisor especificado no participo en el viaje"
            )


class ReviewListSerializer(serializers.ModelSerializer):
    """
    This serializer handles the serialization of Review instances for the list and retrieve action.

    Methods:
        get_reviewer():
            Returns the full name of the reviewer.
    """

    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    reviewer = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ["id", "user", "reviewer", "trip", "rating", "comment"]
        read_only_fields = ["id", "user", "reviewer", "trip", "rating", "comment"]

    def get_reviewer(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
