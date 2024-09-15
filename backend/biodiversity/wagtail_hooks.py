from wagtail import hooks
from wagtail.admin.panels import TitleFieldPanel, FieldPanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import Plant

@hooks.register("register_icons")
def register_icons(icons):
    return icons + ['biodiversity/icons/plant.svg']


class PlantViewSet(SnippetViewSet):
    model = Plant
    icon = "plant"
    add_to_admin_menu = True

    panels = [
        TitleFieldPanel("name"),
        FieldPanel("description"),
    ]

register_snippet(PlantViewSet)
