from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .viewsets import UserPlantViewSet

router = DefaultRouter()
router.register(r'plants', UserPlantViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
