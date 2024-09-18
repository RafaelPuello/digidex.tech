from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import Plant


class PlantViewSet(SnippetViewSet):
    model = Plant
    icon = "plant"
    menu_label = "Plants"
    menu_name = "plants"

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
        InlinePanel("gallery_images", label="Images"),
        InlinePanel("documents", label="Documents"),
    ]
