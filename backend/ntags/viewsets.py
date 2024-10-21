from wagtail.admin.panels import TabbedInterface, FieldPanel, ObjectList, InlinePanel
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup  # noqa

from .models import NFCTag, NFCTagDesign


class NFCTagSnippetViewSet(SnippetViewSet):

    model = NFCTag
    add_to_admin_menu = True
    copy_view_enabled = False
    menu_icon = "nfc-logo"
    menu_label = "NFC Tags"
    menu_name = "nfc-tags"
    menu_order = 131
    url_namespace = "nfc_tags"
    url_prefix = "nfc-tags"
    list_display = ["design"]
    list_per_page = 25
    list_filter = {
        "design": ["exact"],
    }

    content_panels = [
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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if qs is None:
            qs = self.model.objects.all()

        return qs.filter(user=request.user)


class NFCTagDesignSnippetViewSet(SnippetViewSet):

    model = NFCTagDesign
    add_to_admin_menu = True
    copy_view_enabled = False
    menu_icon = "nfc-design"
    menu_label = "NFC Tag Designs"
    menu_name = "nfc-tag-designs"
    menu_order = 132
    url_namespace = "nfc_tag_designs"
    url_prefix = "nfc-tag-designs"
    list_filter = {"name": ["icontains"]}
    list_display = ["name", "description"]
    list_per_page = 25

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
