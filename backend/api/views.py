from rest_framework import routers

from nearfieldcommunication.viewsets import NfcTagViewSet, NfcTagTypeViewSet
from assistant.viewsets import UserAssistantDetail
from inventory.viewsets import InventoryBoxAPIViewSet

router = routers.DefaultRouter()
router.register(r'ntags', NfcTagViewSet)
router.register(r'ntag-types', NfcTagTypeViewSet)
router.register(r'assistants', UserAssistantDetail)
router.register(r'inventories', InventoryBoxAPIViewSet)
