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

    def get_queryset(self):
        """
        Filter to only show NFC tags for the current user if they're not a superuser.
        """
        if self.request.user.is_superuser:
            return super().get_queryset()
        return super().get_queryset().filter(user=self.request.user)


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

    def get_queryset(self):
        """
        Filter to only show NFC tags for the current user if they're not a superuser.
        """
        if self.request.user.is_superuser:
            return NfcTag.objects.all()
        return NfcTag.objects.filter(user=self.request.user)


class NfcTagViewSetGroup(SnippetViewSetGroup):
    items = [NfcTagViewSet, NfcTagTypeViewSet, NfcTagScanViewSet]
    menu_icon = "nfc-icon"
    menu_label = "NFC Tags"
    menu_name = "nfc tags"
    add_to_admin_menu = True

register_snippet(NfcTagViewSetGroup)
