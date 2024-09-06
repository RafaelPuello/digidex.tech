from wagtail.api.v2.router import WagtailAPIRouter

from inventory.api import UserInventoryAPIViewSet, InventoryEntityAPIViewSet, EntityGalleryImageAPIViewSet
from assistant.api import UserAssistantDetail

api_router = WagtailAPIRouter('wagtailapi')
api_router.register_endpoint("inventories", UserInventoryAPIViewSet)
api_router.register_endpoint("entities", InventoryEntityAPIViewSet)
api_router.register_endpoint("images", EntityGalleryImageAPIViewSet)
api_router.register_endpoint('assistants', UserAssistantDetail)
