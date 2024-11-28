from rest_framework import routers

from .views import CustomUserViewSet, StateViewSet


router = routers.SimpleRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'states', StateViewSet)
urlpatterns = router.urls
