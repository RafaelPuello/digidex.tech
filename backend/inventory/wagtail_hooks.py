from wagtail.admin.panels import TitleFieldPanel, FieldPanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import TrainerInventory, InventoryPlant


class TrainerInventoryViewSet(SnippetViewSet):
    model = TrainerInventory

    panels = [
        TitleFieldPanel("name"),
        FieldPanel("description"),
    ]


class InventoryPlantViewSet(SnippetViewSet):
    model = InventoryPlant

    panels = [
        FieldPanel("inventory"),
        MultiFieldPanel(
            [
                FieldPanel("label"),
                FieldPanel("nfc_tag"),
            ],
            heading="Plant Details"
        ),
        FieldPanel("plant"),
    ]

register_snippet(TrainerInventoryViewSet)
register_snippet(InventoryPlantViewSet)
