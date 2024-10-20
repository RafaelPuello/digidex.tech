from wagtail.admin.panels import TabbedInterface, FieldPanel, FieldRowPanel, InlinePanel, ObjectList
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import UserPlant


class UserPlantViewSet(SnippetViewSet):
    model = UserPlant
    icon = "plant"
    menu_label = "Plants"
    menu_name = "plants"
    menu_order = 120
    copy_view_enabled = False
    admin_url_namespace = "inventory_plants"
    list_display = ["name", "description"]
    list_per_page = 50
    admin_url_namespace = "plants"
    base_url_path = "inventory/plants"
    add_to_admin_menu = True

    content_panels = [
        FieldRowPanel([
            FieldPanel("box"),
            FieldPanel("name"),
        ]),
        FieldPanel("description"),
        FieldPanel("species"),
        FieldPanel("copies"),
    ]

    journal_panels = [
        FieldPanel("notes", classname="collapsed"),
        InlinePanel("gallery_images", label="Image Gallery", classname="collapsed"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading='Details'),
            ObjectList(journal_panels, heading='Journal'),
        ]
    )

    def get_queryset(self, request):
        queryset = UserPlant.objects.filter(box__owner=request.user)
        return queryset
