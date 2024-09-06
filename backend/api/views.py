from rest_framework import routers
from wagtail.api.v2.router import WagtailAPIRouter

from nearfieldcommunication.viewsets import NfcTagViewSet, NfcTagTypeViewSet
from assistant.viewsets import UserAssistantDetail
from inventory.viewsets import UserInventoryAPIViewSet, InventoryEntityAPIViewSet, EntityGalleryImageAPIViewSet

router = routers.DefaultRouter()
router.register(r'nfc-tags', NfcTagViewSet)
router.register(r'nfc-tag-types', NfcTagTypeViewSet)
router.register(r'assistant', UserAssistantDetail)

api_router = WagtailAPIRouter('wagtailapi')
api_router.register_endpoint("inventories", UserInventoryAPIViewSet)
api_router.register_endpoint("entities", InventoryEntityAPIViewSet)
api_router.register_endpoint("images", EntityGalleryImageAPIViewSet)
