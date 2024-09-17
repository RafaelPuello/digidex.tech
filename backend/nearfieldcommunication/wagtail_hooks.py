from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from .models import NfcTag, NfcTagType, NfcTagScan


class NfcTagViewSet(SnippetViewSet):
    model = NfcTag
    icon = "tag"
    menu_label = "Tags"
    menu_name = "tags"

    panels = [
        FieldPanel("label"),
    ]


class NfcTagTypeViewSet(SnippetViewSet):
    model = NfcTagType
    icon = "tag"
    menu_label = "Tag Types"
    menu_name = "types"

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
    ]


class NfcTagScanViewSet(SnippetViewSet):
    model = NfcTagScan
    icon = "tag"
    menu_label = "Tag Scans"
    menu_name = "scans"

    panels = [
    ]


class NfcTagViewSetGroup(SnippetViewSetGroup):
    items = [NfcTagViewSet, NfcTagTypeViewSet, NfcTagScanViewSet]
    menu_icon = "tag"
    menu_label = "NFC Tags"
    menu_name = "nfc tags"
    add_to_admin_menu = True

register_snippet(NfcTagViewSetGroup)
