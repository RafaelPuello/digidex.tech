from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import InventoryBox


class InventoryBoxViewSet(SnippetViewSet):
    model = InventoryBox
    icon = "desktop"
    name = "Inventory"
    add_to_admin_menu = True

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
    ]

register_snippet(InventoryBoxViewSet)
