from wagtail import hooks
from wagtail.admin.panels import TabbedInterface, FieldPanel, ObjectList
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from .models import NFCTag, NFCTagType, NFCTagScan, NFCTagMemory


@hooks.register("register_icons")
def register_icons(icons):
    return icons + [
        'ntags/icons/nfc-icon.svg',
        'ntags/icons/nfc-types.svg',
        'ntags/icons/nfc-scan.svg',
        'ntags/icons/nfc-memory.svg',
    ]


class NfcTagTypeSnippetViewSet(SnippetViewSet):
    """
    A snippetviewset for viewing and editing the types of NFC Tag.
    """
    model = NFCTagType
    icon = "nfc-types"
    menu_label = "Tag Types"
    menu_name = "types"
    copy_view_enabled = False
    list_filter = {"name": ["exact"], "description": ["icontains"]}
    list_display = ["name"]
    list_per_page = 25
    admin_url_namespace = "nfc_types"
    base_url_path = "nfc-types"

    shared_panels = [
        FieldPanel("name"),
        FieldPanel("description"),
    ]
    private_panels = []

    edit_handler = TabbedInterface(
        [
            ObjectList(shared_panels, heading='Details'),
            ObjectList(private_panels, heading='Admin only', permission="superuser"),
        ]
    )


class NFCTagSnippetViewSet(SnippetViewSet):
    """
    A snippetviewset for viewing and editing NFC Tags.
    """
    model = NFCTag
    icon = "tag"
    menu_label = "Tags"
    menu_name = "tags"
    copy_view_enabled = False
    list_filter = {"nfc_tag_type": ["exact"], "label": ["icontains"]}
    list_display = ["label", "nfc_tag_type", "serial_number"]
    list_per_page = 25
    admin_url_namespace = "nfc_tags"
    base_url_path = "nfc-tags"

    shared_panels = [
        FieldPanel("label")
    ]
    private_panels = [
        FieldPanel("user"),
        FieldPanel("nfc_tag_type"),
        FieldPanel("active"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(shared_panels, heading='Details'),
            ObjectList(private_panels, heading='Admin only', permission="superuser"),
        ]
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if qs is None:
            qs = self.model.objects.all()
        
        user = request.user
        if user.is_superuser:
            return qs
        else:
            return qs.filter(user=user)


class NFCTagScanSnippetViewSet(SnippetViewSet):
    """
    A snippetviewset for viewing and editing NFC Tag scans.
    """
    model = NFCTagScan
    icon = "nfc-scan"
    menu_label = "Tag Scans"
    menu_name = "scans"
    copy_view_enabled = False
    # list_filter = {"nfc_tag": ["exact"], "scanned_by": ["exact"], "scanned_at": ["date"]}
    list_display = ["nfc_tag", "counter", "scanned_by", "scanned_at"]
    list_per_page = 25
    admin_url_namespace = "nfc_scans"
    base_url_path = "nfc/scans"

    shared_panels = []
    private_panels = []

    edit_handler = TabbedInterface(
        [
            ObjectList(shared_panels, heading='Details'),
            ObjectList(private_panels, heading='Admin only', permission="superuser"),
        ]
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if qs is None:
            qs = self.model.objects.all()
        
        user = request.user
        if user.is_superuser:
            return qs
        else:
            return qs.filter(nfc_tag__user=user)


class NFCTagMemorySnippetViewSet(SnippetViewSet):
    """
    A snippetviewset for viewing and editing NFC Tag memory.
    """
    model = NFCTagMemory
    icon = "nfc-memory"
    menu_label = "Tag Memory"
    menu_name = "memory"
    copy_view_enabled = False
    # list_filter = {"nfc_tag": ["exact"]}
    list_display = ["nfc_tag", "last_modified"]
    list_per_page = 25
    admin_url_namespace = "nfc_memory"
    base_url_path = "nfc/memory"

    shared_panels = []
    private_panels = []

    edit_handler = TabbedInterface(
        [
            ObjectList(shared_panels, heading='Details'),
            ObjectList(private_panels, heading='Admin only', permission="superuser"),
        ]
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if qs is None:
            qs = self.model.objects.all()

        user = request.user
        if user.is_superuser:
            return qs
        else:
            return qs.filter(nfc_tag__user=user)


class NFCTagSnippetViewSetGroup(SnippetViewSetGroup):
    """
    A snippetviewset group for NFC Tags.
    """
    items = [NFCTagSnippetViewSet, NfcTagTypeSnippetViewSet, NFCTagScanSnippetViewSet, NFCTagMemorySnippetViewSet]
    menu_icon = "nfc-icon"
    menu_label = "NFC Tags"
    menu_name = "nfc_tags"
    add_to_admin_menu = True


register_snippet(NFCTagSnippetViewSetGroup)