from wagtail.admin.panels import TabbedInterface, InlinePanel, FieldPanel, ObjectList
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import Plant


class PlantViewSet(SnippetViewSet):
    model = Plant
    icon = "plant"
    menu_label = "Plants"
    menu_name = "plants"

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
