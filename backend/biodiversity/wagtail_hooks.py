from wagtail import hooks
from wagtail.admin.panels import TabbedInterface, InlinePanel, FieldPanel, ObjectList
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import Plant


@hooks.register("register_icons")
def register_icons(icons):
    return icons + ['biodiversity/icons/plant.svg']


class PlantSnippetViewSet(SnippetViewSet):
    model = Plant
    icon = "plant"
    menu_label = "Plants"
    menu_name = "plants"

    shared_panels = [
        FieldPanel("name"),
        FieldPanel("description"),
        InlinePanel("images", label="Plant Images"),
        InlinePanel("documents", label="Plant Documents"),
    ]

    private_panels = [
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(shared_panels, heading='Details'),
            ObjectList(private_panels, heading='Admin only', permission="superuser"),
        ]
    )
