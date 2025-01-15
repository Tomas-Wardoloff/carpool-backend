from django.urls import path, include
from rest_framework import routers

from .views import (
    CustomUserViewSet,
    StateViewSet,
    CityViewSet,
    VehicleViewSet,
    TripParticipantViewSet,
    TripViewSet,
    TripJoinRequestViewSet,
)


router = routers.SimpleRouter()
router.register(r"users", CustomUserViewSet)
router.register(r"states", StateViewSet)
router.register(r"cities", CityViewSet)
router.register(r"vehicles", VehicleViewSet)
router.register(r"participants", TripParticipantViewSet)
router.register(r"trips", TripViewSet)
router.register(r"join-requests", TripJoinRequestViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("trips/<int:trip_pk>/join-requests/", TripJoinRequestViewSet.as_view({"get": "list"})),
]
