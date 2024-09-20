from wagtail import hooks
from wagtail.admin.panels import TabbedInterface, FieldPanel, ObjectList
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from .models import NFCTag, NFCTagDesign, NFCTagScan, NFCTagEEPROM


@hooks.register("register_icons")
def register_icons(icons):
    return icons + [
        'ntags/icons/ntag.svg',
        'ntags/icons/design.svg',
        'ntags/icons/eeprom.svg',
        'ntags/icons/scan.svg'
    ]


class NFCTagDesignSnippetViewSet(SnippetViewSet):
    """
    A snippetviewset for viewing and editing the designs of NFC Tags.
    """
    model = NFCTagDesign
    icon = "design"
    menu_label = "Tag Designs"
    menu_name = "designs"
    copy_view_enabled = False
    list_filter = {"name": ["exact"], "description": ["icontains"]}
    list_display = ["name"]
    list_per_page = 25
    admin_url_namespace = "ntag_designs"
    base_url_path = "ntags/designs"

    public_panels = [
        FieldPanel("name"),
        FieldPanel("description"),
    ]

    private_panels = [
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(public_panels, heading='Details'),
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
    list_filter = {"design": ["exact"]}
    list_display = ["serial_number", "design"]
    list_per_page = 25
    admin_url_namespace = "ntags"
    base_url_path = "ntags/tags"

    public_panels = [
    ]

    private_panels = [
        FieldPanel("user"),
        FieldPanel("design"),
        FieldPanel("content"),
        FieldPanel("active"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(public_panels, heading='Details'),
            ObjectList(private_panels, heading='Admin only', permission="superuser"),
        ]
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if qs is None:
            qs = self.model.objects.all()
        return qs.filter(user=request.user)


class NFCTagScanSnippetViewSet(SnippetViewSet):
    """
    A snippetviewset for viewing and editing NFC Tag scans.
    """
    model = NFCTagScan
    icon = "scan"
    menu_label = "Tag Scans"
    menu_name = "scans"
    copy_view_enabled = False
    # list_filter = {"ntag": ["exact"], "scanned_by": ["exact"], "scanned_at": ["date"]}
    list_display = ["ntag", "counter", "scanned_by", "scanned_at"]
    list_per_page = 25
    admin_url_namespace = "ntag_scans"
    base_url_path = "ntags/scans"

    public_panels = [
    ]

    private_panels = [
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(public_panels, heading='Details'),
            ObjectList(private_panels, heading='Admin only', permission="superuser"),
        ]
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if qs is None:
            qs = self.model.objects.all()
        return qs.filter(ntag__user=request.user)


class NFCTagEEPROMSnippetViewSet(SnippetViewSet):
    """
    A snippetviewset for viewing and editing NFC Tag eeprom.
    """
    model = NFCTagEEPROM
    icon = "eeprom"
    menu_label = "Tag EEPROM"
    menu_name = "eeprom"
    copy_view_enabled = False
    # list_filter = {"ntag": ["exact"]}
    list_display = ["ntag", "last_modified"]
    list_per_page = 25
    admin_url_namespace = "ntag_eeprom"
    base_url_path = "ntags/eeprom"

    public_panels = [
    ]

    private_panels = [
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(public_panels, heading='Details'),
            ObjectList(private_panels, heading='Admin only', permission="superuser"),
        ]
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if qs is None:
            qs = self.model.objects.all()
        return qs.filter(ntag__user=request.user)


class NfcTagSnippetViewSetGroup(SnippetViewSetGroup):
    """
    A snippetviewset group for NFC Tags.
    """
    items = [NFCTagSnippetViewSet, NFCTagDesignSnippetViewSet, NFCTagScanSnippetViewSet, NFCTagEEPROMSnippetViewSet]
    menu_icon = "ntag"
    menu_label = "NFC Tags"
    menu_name = "ntags"
    add_to_admin_menu = True


register_snippet(NfcTagSnippetViewSetGroup)
