from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .viewsets import NFCTagViewSet

app_name = "ntags"

router = DefaultRouter()
router.register(r'ntags', NFCTagViewSet, basename='ntag')

urlpatterns = [
    path('', include(router.urls)),
]
