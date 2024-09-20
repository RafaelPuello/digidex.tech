from wagtail.admin.panels import TabbedInterface, FieldPanel, ObjectList
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from botany.wagtail_hooks import PlantSnippetViewSet
from .models import Box


class BoxSnippetViewSet(SnippetViewSet):
    """
    A snippet view set for the Box model.
    """
    model = Box
    icon = "folder"
    menu_label = "Boxes"
    menu_name = "boxes"

    shared_panels = [
        FieldPanel("name"),
        FieldPanel("description"),
    ]

    private_panels = [
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(shared_panels, heading='Details'),
            ObjectList(private_panels, heading='Admin only', permission="superuser"),
        ]
    )


class InventorySnippetViewSetGroup(SnippetViewSetGroup):
    """
    A snippet view set group for the Plant and Box models.
    """
    items = [PlantSnippetViewSet, BoxSnippetViewSet]
    menu_icon = "desktop"
    menu_label = "Inventory"
    menu_name = "inventory"
    add_to_admin_menu = True


register_snippet(InventorySnippetViewSetGroup)
