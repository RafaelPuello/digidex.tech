from rest_framework import routers

from nearfieldcommunication.viewsets import NfcTagViewSet, NfcTagTypeViewSet
from assistant.viewsets import TrainerAssistantDetail
from inventory.viewsets import TrainerInventoryAPIViewSet

router = routers.DefaultRouter()
router.register(r'ntags', NfcTagViewSet)
router.register(r'ntag-types', NfcTagTypeViewSet)
router.register(r'assistant', TrainerAssistantDetail)
router.register(r'inventories', TrainerInventoryAPIViewSet)
