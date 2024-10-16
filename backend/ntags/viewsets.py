from wagtail.admin.panels import TabbedInterface, FieldPanel, ObjectList, InlinePanel
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from .models import NFCTag, NFCTagDesign, NFCTagScan
from .forms import NFCTagAdminForm


class NFCTagSnippetViewSet(SnippetViewSet):

    model = NFCTag
    icon = "tag"
    menu_label = "Tags"
    menu_name = "tags"
    menu_order = 131
    copy_view_enabled = False
    admin_url_namespace = "nfc_tags"
    base_url_path = "nfc-tags/tags"
    list_display = ["label", "design"]
    list_per_page = 25
    list_filter = {
        "label": ["icontains"],
        "design": ["exact"],
    }

    content_panels = [
        FieldPanel("label"),
        FieldPanel("content_type"),
        FieldPanel("item")
    ]

    settings_panels = [
        FieldPanel("active"),
        FieldPanel("design")
    ]
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading='Details'),
            ObjectList(settings_panels, heading='Status'),
        ]
    )

    def get_form_class(self, for_update=False):
        return NFCTagAdminForm

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if qs is None:
            qs = self.model.objects.all()

        return qs.filter(user=request.user)


class NFCTagDesignSnippetViewSet(SnippetViewSet):

    model = NFCTagDesign
    icon = "nfc-design"
    menu_label = "Designs"
    menu_name = "designs"
    menu_order = 133
    copy_view_enabled = False
    list_filter = {"name": ["icontains"]}
    list_display = ["name", "description"]
    list_per_page = 25
    admin_url_namespace = "nfc_tag_designs"
    base_url_path = "nfc-tags/designs"

    content_panels = [
        FieldPanel("name"),
        FieldPanel("description"),
        InlinePanel("gallery_images")
    ]

    settings_panels = [
        FieldPanel("designer")
    ]
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading='Details'),
            ObjectList(settings_panels, heading='Status'),
        ]
    )


class NFCTagScanSnippetViewSet(SnippetViewSet):

    model = NFCTagScan
    icon = "nfc-scan"
    menu_label = "Scans"
    menu_name = "scans"
    menu_order = 135
    copy_view_enabled = False
    list_filter = {"nfc_tag": ["exact"]}
    list_display = ["nfc_tag", "counter", "scanned_at"]
    list_per_page = 100
    admin_url_namespace = "nfc_tag_scans"
    base_url_path = "nfc-tags/scans"

    content_panels = [
        FieldPanel("nfc_tag"),
        FieldPanel("counter"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading='Details'),
        ]
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if qs is None:
            qs = self.model.objects.all()

        return qs.filter(nfc_tag__user=request.user)


class NFCTagSnippetViewSetGroup(SnippetViewSetGroup):
    items = (NFCTagSnippetViewSet, NFCTagDesignSnippetViewSet, NFCTagScanSnippetViewSet)
    add_to_admin_menu = True
    menu_icon = "nfc-logo"
    menu_label = "NFC Tags"
    menu_name = "nfc-tags"
    menu_order = 130
