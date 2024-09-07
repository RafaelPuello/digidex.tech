from rest_framework import routers

from nearfieldcommunication.viewsets import NfcTagViewSet, NfcTagTypeViewSet
from assistant.viewsets import UserAssistantDetail
from inventory.viewsets import TrainerInventoryAPIViewSet

router = routers.DefaultRouter()
router.register(r'nfc-tags', NfcTagViewSet)
router.register(r'nfc-tag-types', NfcTagTypeViewSet)
router.register(r'assistant', UserAssistantDetail)
router.register(r'inventories', TrainerInventoryAPIViewSet)
