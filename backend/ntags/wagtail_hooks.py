from wagtail import hooks
from wagtail.admin.panels import TabbedInterface, FieldPanel, ObjectList
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from .models import NFCTag, NFCTagDesign, NFCTagScan, NFCTagMemory


@hooks.register("register_icons")
def register_icons(icons):
    return icons + [
        'ntags/icons/ntag.svg',
        'ntags/icons/design.svg',
        'ntags/icons/memory.svg',
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


class NFCTagSnippetViewSet(SnippetViewSet):
    """
    A snippetviewset for viewing and editing NFC Tags.
    """

    model = NFCTag
    icon = "tag"
    menu_label = "Tags"
    menu_name = "tags"
    copy_view_enabled = False
    list_filter = {"design": ["exact"], "label": ["icontains"]}
    list_display = ["label", "design", "serial_number"]
    list_per_page = 25
    admin_url_namespace = "ntags"
    base_url_path = "ntags/tags"

    shared_panels = [
        FieldPanel("label")
    ]

    private_panels = [
        FieldPanel("user"),
        FieldPanel("design"),
        FieldPanel("active"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(shared_panels, heading='Details'),
            ObjectList(private_panels, heading='Admin only', permission="superuser"),
        ]
    )

    def get_queryset(self, request):
        """
        Filter NFC tags based on user roles:
        """

        qs = super().get_queryset(request)
        if qs is None:
            qs = self.model.objects.all()
        user = request.user

        if user.is_superuser:
            return qs
        elif user.groups.filter(name='Trainers').exists():
            return qs.filter(user=user)
        else:
            return qs.none()


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

    def get_queryset(self, request):
        """
        Filter NFC tag scans based on user roles:
        - Superusers see all tag scans.
        - Trainers see tag scans associated with their tags.
        - Others see no tag scans.
        """

        qs = super().get_queryset(request)
        if qs is None:
            qs = self.model.objects.all()
        user = request.user

        if user.is_superuser:
            return qs
        elif user.groups.filter(name='Trainers').exists():
            return qs.filter(nfc_tag__user=user)
        else:
            return qs.none()


class NFCTagMemorySnippetViewSet(SnippetViewSet):
    """
    A snippetviewset for viewing and editing NFC Tag memory.
    """

    model = NFCTagMemory
    icon = "memory"
    menu_label = "Tag Memory"
    menu_name = "memory"
    copy_view_enabled = False
    # list_filter = {"nfc_tag": ["exact"]}
    list_display = ["nfc_tag", "last_modified"]
    list_per_page = 25
    admin_url_namespace = "ntag_memory"
    base_url_path = "ntags/memory"

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

    def get_queryset(self, request):
        """
        Filter NFC tag memory based on user roles:
        - Superusers see all tag memories.
        - Trainers see tag memories associated with their tags.
        - Others see no tag memories.
        """

        qs = super().get_queryset(request)
        if qs is None:
            qs = self.model.objects.all()
        user = request.user

        if user.is_superuser:
            return qs
        elif user.groups.filter(name='Trainers').exists():
            return qs.filter(ntag__user=user)
        else:
            return qs.none()


class NfcTagSnippetViewSetGroup(SnippetViewSetGroup):
    """
    A snippetviewset group for NFC Tags.
    """

    items = [NFCTagSnippetViewSet, NFCTagDesignSnippetViewSet, NFCTagScanSnippetViewSet, NFCTagMemorySnippetViewSet]
    menu_icon = "ntag"
    menu_label = "NFC Tags"
    menu_name = "nfc_tags"
    add_to_admin_menu = True


register_snippet(NfcTagSnippetViewSetGroup)
