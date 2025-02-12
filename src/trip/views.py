from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import (
    StateSerializer,
    CitySerializer,
    VehicleDetailSerializer,
    VehicleListSerializer,
    TripParticipantDetailSerializer,
    TripParticipantListSerializer,
    TripDetailSerializer,
    TripListSerializer,
    TripJoinRequestSerializer,
)
from .models import State, City, Vehicle, Trip, TripParticipant, TripJoinRequest


class StateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset provides `list` and `retrieve` actions.
    All actions require authentication
    The states can only be created by an admin users outside the API.
    """

    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [IsAuthenticated]


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset provides `list` and `retrieve` actions.
    All actions require authentication
    The cities can only be created by an admin users outside the API.
    """

    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated]


class VehicleViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `create`, `retrieve`, `update`, `partial_update`, `destroy`, and `list` actions.
    The `create` action assigns the authenticated user as the owner of the vehicle.
    """

    queryset = Vehicle.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action in ("retrieve", "update", "partial_update", "destroy"):
            return Vehicle.objects.filter(owner=self.request.user)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "retrieve"):
            return VehicleDetailSerializer
        return VehicleListSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TripParticipantViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `create`, `retrieve`, `update`, `partial_update`, `destroy`, and `list` actions.
    The `create` action ensures that a user can only participate in a trip once.

    Methods:
        get_queryset():
            Returns the queryset of TripParticipant instances filtered by the authenticated user.
        get_serializer_class():
            Returns the appropriate serializer class depending on the action.
        perform_create():
            Raises a PermissionDenied exception to prevent the creation of a TripParticipant instance.
        update():
            Raises a PermissionDenied exception to prevent updating a TripParticipant instance.
        partial_update():
            Raises a PermissionDenied exception to prevent updating a TripParticipant instance.
    """

    queryset = TripParticipant.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action in ("retrieve", "update", "partial_update", "destroy"):
            return TripParticipant.objects.filter(user=self.request.user)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "retrieve"):
            return TripParticipantDetailSerializer
        return TripParticipantListSerializer

    def perform_create(self, serializer):
        raise PermissionDenied(
            "No puedes crear un participante, solo puedes unirte a un viaje a través de una solicitud."
        )

    def update(self, request, *args, **kwargs):
        raise PermissionDenied(
            "No puedes actualizar un participante, solo puedes crear o eliminar."
        )

    def partial_update(self, request, *args, **kwargs):
        raise PermissionDenied(
            "No puedes actualizar un participante, solo puedes crear o eliminar."
        )


class TripViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `create`, `retrieve`, `update`, `partial_update`, `destroy`, and `list` actions.
    The `create` action assigns the authenticated user as the creator of the trip and adds them as a participant with the role of 'driver'.

    Methods:
        get_permissions():
            Returns the appropriate permission class depending on the action.
        get_queryset():
            Returns the queryset of Trip instances filtered by the authenticated user depending on the action.
        get_serializer_class():
            Returns the appropriate serializer class depending on the action.
        perform_create():
            Creates a TripParticipant instance with the authenticated user as the driver of the trip.
    """

    queryset = Trip.objects.all()

    def get_permissions(self):
        if self.action == "list":
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        if self.action in ("update", "partial_update", "destroy"):
            return Trip.objects.filter(creator=self.request.user)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return TripDetailSerializer
        return TripListSerializer

    def perform_create(self, serializer):
        trip = serializer.save(creator=self.request.user)
        TripParticipant.objects.create(trip=trip, user=self.request.user, role="driver")


class TripJoinRequestViewSet(viewsets.ModelViewSet):
    """"""

    queryset = TripJoinRequest.objects.all()
    serializer_class = TripJoinRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        trip_id = self.kwargs.get("trip_pk")
        if trip_id:
            return TripJoinRequest.objects.filter(trip__creator=user, trip=trip_id)
        return TripJoinRequest.objects.filter(trip__creator=user)
