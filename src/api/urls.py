from rest_framework import routers

from .views import CustomUserViewSet, StateViewSet, CityViewSet


router = routers.SimpleRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'states', StateViewSet)
router.register(r'cities', CityViewSet)
urlpatterns = router.urls
