from wagtail.admin.panels import TabbedInterface, FieldPanel, ObjectList
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import NFCTag
from .forms import NFCTagAdminForm


class NFCTagSnippetViewSet(SnippetViewSet):

    model = NFCTag
    icon = "nfc-icon"
    menu_label = "NFC Tags"
    menu_name = "ntags"
    menu_order = 130
    copy_view_enabled = False
    list_filter = {"label": ["icontains"]}
    list_display = ["label", "serial_number"]
    list_per_page = 25
    admin_url_namespace = "nfc_tags"
    base_url_path = "nfc-tags"
    add_to_admin_menu = True

    content_panels = [
        FieldPanel("label"),
        FieldPanel("content_type"),
        FieldPanel("item")
    ]

    settings_panels = [
        FieldPanel("active")
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

        user = request.user
        if user.is_superuser:
            return qs
        else:
            return qs.filter(user=user)
