from rest_framework import routers

from .viewsets import PlantViewSet

router = routers.DefaultRouter()
router.register(r'plants', PlantViewSet)
