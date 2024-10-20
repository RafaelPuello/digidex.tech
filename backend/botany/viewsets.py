from wagtail.admin.panels import MultiFieldPanel, FieldPanel, FieldRowPanel
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

    panels = [
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel("box", classname="col3"),
                FieldPanel("species", classname="col3"),
                FieldPanel("taxon_id", classname="col1"),
                FieldPanel("name", classname="col5"),
            ]),
            FieldPanel("description"),
            FieldPanel("image"),
        ]),
        FieldPanel("copies", classname="collapsed"),
    ]

    def get_queryset(self, request):
        queryset = UserPlant.objects.filter(box__owner=request.user)
        return queryset
