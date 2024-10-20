from django.templatetags.static import static
from django.utils.html import format_html
from wagtail import hooks
from wagtail.admin.panels import TabbedInterface, FieldPanel, ObjectList, InlinePanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from .models import NFCTag, NFCTagDesign
from .forms import NFCTagAdminForm


@hooks.register("insert_editor_js")
def editor_js():
    return format_html('<script src="{}"></script>', static("nfctags/js/nfc-tag-editor.js"))


@hooks.register("register_icons")
def register_icons(icons):
    return icons + [
        'nfctags/icons/logo.svg',
        'nfctags/icons/designs.svg',
        'nfctags/icons/scans.svg',
        'nfctags/icons/memory.svg',
    ]


class NFCTagSnippetViewSet(SnippetViewSet):

    model = NFCTag
    icon = "tag"
    menu_label = "Tags"
    menu_name = "tags"
    menu_order = 131
    copy_view_enabled = False
    url_namespace = "nfc_tags"
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
    url_namespace = "nfc_tag_designs"
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


class NFCTagSnippetViewSetGroup(SnippetViewSetGroup):
    items = (NFCTagSnippetViewSet, NFCTagDesignSnippetViewSet)
    add_to_admin_menu = True
    menu_icon = "nfc-logo"
    menu_label = "NFC Tags"
    menu_name = "nfc-tags"
    menu_order = 130


register_snippet(NFCTagSnippetViewSetGroup)  # noqa