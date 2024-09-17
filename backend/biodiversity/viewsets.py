from django.shortcuts import render
from pygbif import species, occurrences
from wagtail.admin.panels import FieldPanel
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
    ]
