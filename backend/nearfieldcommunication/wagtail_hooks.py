from wagtail import hooks
from wagtail.admin.panels import TabbedInterface, FieldPanel, ObjectList
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from .models import NfcTag, NfcTagType, NfcTagScan

@hooks.register("register_icons")
def register_icons(icons):
    return icons + [
        'nearfieldcommunication/icons/nfc-icon.svg',
        'nearfieldcommunication/icons/nfc-types.svg',
        'nearfieldcommunication/icons/nfc-scan.svg'
        ]


class NfcTagViewSet(SnippetViewSet):
    model = NfcTag
    icon = "tag"
    menu_label = "Tags"
    menu_name = "tags"

    shared_panels = [
    
    ]

    private_panels = [
        FieldPanel("user"),
        FieldPanel("nfc_tag_type"),
        FieldPanel("url"),
        FieldPanel("active"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(shared_panels, heading='Details'),
            ObjectList(private_panels, heading='Admin only', permission="superuser"),
        ]
    )


class NfcTagTypeViewSet(SnippetViewSet):
    model = NfcTagType
    icon = "nfc-types"
    menu_label = "Tag Types"
    menu_name = "types"

    shared_panels = [
        FieldPanel("name"),
        FieldPanel("description"),   
    ]

    private_panels = [
        FieldPanel("integrated_circuit"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(shared_panels, heading='Details'),
            ObjectList(private_panels, heading='Admin only', permission="superuser"),
        ]
    )


class NfcTagScanViewSet(SnippetViewSet):
    model = NfcTagScan
    icon = "nfc-scan"
    menu_label = "Tag Scans"
    menu_name = "scans"

    shared_panels = [
    
    ]

    private_panels = [
    
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(shared_panels, heading='Details'),
            ObjectList(private_panels, heading='Admin only', permission="superuser"),
        ]
    )


class NfcTagViewSetGroup(SnippetViewSetGroup):
    items = [NfcTagViewSet, NfcTagTypeViewSet, NfcTagScanViewSet]
    menu_icon = "nfc-icon"
    menu_label = "NFC Tags"
    menu_name = "nfc tags"
    add_to_admin_menu = True

register_snippet(NfcTagViewSetGroup)
