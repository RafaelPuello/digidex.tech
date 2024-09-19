from rest_framework import routers

from accounts.viewsets import UserViewSet
from ntags.viewsets import NFCTagViewSet, NFCTagDesignViewSet
from assistants.viewsets import UserAssistantDetail
from inventory.viewsets import BoxViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'ntags', NFCTagViewSet)
router.register(r'ntag-designs', NFCTagDesignViewSet)
router.register(r'assistants', UserAssistantDetail)
router.register(r'boxes', BoxViewSet)
