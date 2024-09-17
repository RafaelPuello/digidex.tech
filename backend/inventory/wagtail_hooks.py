from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import Box


class BoxViewSet(SnippetViewSet):
    model = Box
    icon = "desktop"
    name = "Inventory"
    add_to_admin_menu = True

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
    ]

register_snippet(BoxViewSet)
