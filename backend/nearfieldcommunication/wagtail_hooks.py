from wagtail import hooks
from wagtail.admin.panels import TabbedInterface, FieldPanel, ObjectList
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from .models import NfcTag, NfcTagType, NfcTagScan, NfcTagMemory


@hooks.register("register_icons")
def register_icons(icons):
    return icons + [
        'nearfieldcommunication/icons/nfc-icon.svg',
        'nearfieldcommunication/icons/nfc-types.svg',
        'nearfieldcommunication/icons/nfc-scan.svg',
        'nearfieldcommunication/icons/nfc-memory.svg',
    ]


class NfcTagSnippetViewSet(SnippetViewSet):
    model = NfcTag
    icon = "tag"
    menu_label = "Tags"
    menu_name = "tags"

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
        elif user.groups.filter(name='Trainers').exists():
            return qs.filter(user=user)
        else:
            return qs.none()


class NfcTagTypeSnippetViewSet(SnippetViewSet):
    model = NfcTagType
    icon = "nfc-types"
    menu_label = "Tag Types"
    menu_name = "types"

    shared_panels = [
    ]

    private_panels = [
        FieldPanel("name"),
        FieldPanel("description"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(shared_panels, heading='Details'),
            ObjectList(private_panels, heading='Admin only', permission="superuser"),
        ]
    )


class NfcTagScanSnippetViewSet(SnippetViewSet):
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


class NfcTagMemorySnippetViewSet(SnippetViewSet):
    model = NfcTagMemory
    icon = "nfc-memory"
    menu_label = "Tag Memory"
    menu_name = "memory"

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
            return qs.filter(nfc_tag__user=user)
        else:
            return qs.none()


class NfcTagSnippetViewSetGroup(SnippetViewSetGroup):
    items = [NfcTagSnippetViewSet, NfcTagTypeSnippetViewSet, NfcTagScanSnippetViewSet, NfcTagMemorySnippetViewSet]
    menu_icon = "nfc-icon"
    menu_label = "NFC Tags"
    menu_name = "nfc_tags"
    add_to_admin_menu = True


register_snippet(NfcTagSnippetViewSetGroup)
