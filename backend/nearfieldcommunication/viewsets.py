from django.utils.translation import gettext_lazy as _
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup
from wagtail.admin.panels import FieldPanel, TabbedInterface, ObjectList

from .models import NfcTag, NfcTagType


class NfcTagViewSet(SnippetViewSet):
    model = NfcTag
    icon = "tag"
    menu_label = "Your NFC Tags"
    menu_name = "nfc-tags"
    menu_order = 300
    name = "user-nfc-tags"
    admin_url_namespace = "user_nfc_tags"
    base_url_path = "nfc-tag/tags"
    ordering = ["last_modified"]
    list_per_page = 50
    list_display = ("nfc_tag_type", "last_modified")
    list_filter = {
        "nfc_tag_type": ["exact"]
    }

    shared_panels = [
    ]

    private_panels = [
        FieldPanel("nfc_tag_type"),
        FieldPanel("user"),
        FieldPanel("active"),
    ]

    edit_handler = TabbedInterface([
        ObjectList(private_panels, heading='Admin', permission="superuser"),
        ObjectList(shared_panels, heading='Details'),
    ])

    def get_queryset(self, request):
        """
        Filter the queryset to only show instances where the owner is the current user.
        """
        qs = super().get_queryset(request)
        if qs is None:
            user = request.user
            if user.is_superuser:
                qs = self.model.objects.all()
            else:
                qs = self.model.objects.filter(user=request.user)
        return qs


class NfcTagTypeViewSet(SnippetViewSet):
    model = NfcTagType
    icon = "tag"
    add_to_settings_menu = True
    menu_label = "NFC Tag Types"
    menu_name = "nfc-tag-types"
    menu_order = 301
    name = "nfc-tag-types"
    copy_view_enabled = False
    inspect_view_enabled = True
    admin_url_namespace = "nfc_tag_types"
    base_url_path = "nfc-tag/types"
    ordering = ["name"]
    list_per_page = 50
    list_display = ("name", "description", "last_modified")
    list_filter = {
        "name": ["icontains"],
        "description": ["icontains"]
    }

    shared_panels = [
    ]

    private_panels = [
        FieldPanel("name"),
        FieldPanel("description"),
        FieldPanel("integrated_circuit"),
    ]

    edit_handler = TabbedInterface([
        ObjectList(private_panels, heading='Admin', permission="superuser"),
        ObjectList(shared_panels, heading='Details'),
    ])


class NfcViewSetGroup(SnippetViewSetGroup):
    items = (NfcTagTypeViewSet, NfcTagViewSet)
    add_to_admin_menu = True
    menu_icon = "tag"
    menu_label = "Nfc Tags"
    menu_name = "nfc tags"
    menu_order = 250
