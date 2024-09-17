from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from biodiversity.viewsets import PlantViewSet
from .models import Box


class BoxViewSet(SnippetViewSet):
    model = Box
    icon = "folder"
    menu_label = "Boxes"
    menu_name = "boxes"

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
    ]


class InventoryViewSetGroup(SnippetViewSetGroup):
    items = [PlantViewSet, BoxViewSet]
    menu_icon = "desktop"
    menu_label = "Inventory"
    menu_name = "inventory"
    add_to_admin_menu = True

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
    ]


register_snippet(InventoryViewSetGroup)
