from wagtail.admin.panels import TitleFieldPanel, FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import NfcTagType


class NfcTagTypeViewSet(SnippetViewSet):
    model = NfcTagType
    icon = "tag"
    name = "ntag type"
    add_to_admin_menu = True

    panels = [
        TitleFieldPanel("name"),
        FieldPanel("description"),
    ]

register_snippet(NfcTagTypeViewSet)
