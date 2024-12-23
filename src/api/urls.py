from rest_framework import routers

from .views import CustomUserViewSet, StateViewSet, CityViewSet, VehicleViewSet, TripParticipantViewSet, TripViewSet


router = routers.SimpleRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'states', StateViewSet)
router.register(r'cities', CityViewSet)
router.register(r'vehicles', VehicleViewSet)
router.register(r'participants', TripParticipantViewSet)
router.register(r'trips', TripViewSet)
urlpatterns = router.urls
