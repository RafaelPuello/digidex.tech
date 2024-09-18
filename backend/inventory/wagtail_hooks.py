from wagtail.admin.panels import TabbedInterface, InlinePanel, FieldPanel, ObjectList
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from biodiversity.viewsets import PlantViewSet
from .models import Box


class BoxViewSet(SnippetViewSet):
    model = Box
    icon = "folder"
    menu_label = "Boxes"
    menu_name = "boxes"

    shared_panels = [
        FieldPanel("name"),
        FieldPanel("description"),
        InlinePanel("gallery_images", label="Images"),
        InlinePanel("documents", label="Documents"),
    ]

    private_panels = [
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(shared_panels, heading='Details'),
            ObjectList(private_panels, heading='Admin only', permission="superuser"),
        ]
    )


class InventoryViewSetGroup(SnippetViewSetGroup):
    items = [PlantViewSet, BoxViewSet]
    menu_icon = "desktop"
    menu_label = "Inventory"
    menu_name = "inventory"
    add_to_admin_menu = True


register_snippet(InventoryViewSetGroup)
