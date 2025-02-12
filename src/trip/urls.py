from django.urls import path, include
from rest_framework import routers

from .views import (
    StateViewSet,
    CityViewSet,
    VehicleViewSet,
    TripParticipantViewSet,
    TripViewSet,
    TripJoinRequestViewSet,
)


router = routers.SimpleRouter()
router.register(r"states", StateViewSet)
router.register(r"cities", CityViewSet)
router.register(r"vehicles", VehicleViewSet)
router.register(r"participants", TripParticipantViewSet)
router.register(r"trips", TripViewSet)
router.register(r"join-requests", TripJoinRequestViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
