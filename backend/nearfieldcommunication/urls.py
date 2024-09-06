from django.urls import include, path
from rest_framework import routers

from .views import link
from .viewsets import NfcTagViewSet, NfcTagTypeViewSet

app_name = 'nearfieldcommunication'

router = routers.DefaultRouter()
router.register(r'nfc-tags', NfcTagViewSet)
router.register(r'nfc-tag-types', NfcTagTypeViewSet)

urlpatterns = [
    path('link/', link, name='nfc-link'),
    path('api/', include(router.urls)),
]
