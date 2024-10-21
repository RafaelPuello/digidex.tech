from wagtail.admin.panels import FieldPanel
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import NFCTag


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
    list_per_page = 25

    panels = [
        FieldPanel("content_type"),
        FieldPanel("item"),
        FieldPanel("active")
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if qs is None:
            qs = self.model.objects.all()

        return qs.filter(user=request.user)
