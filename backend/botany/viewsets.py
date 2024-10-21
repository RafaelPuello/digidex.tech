from wagtail.admin.panels import MultiFieldPanel, InlinePanel, FieldPanel, FieldRowPanel
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetChooserViewSet

from .models import UserPlant


class UserPlantViewSet(SnippetViewSet):
    model = UserPlant
    icon = "plant"
    menu_label = "Plants"
    menu_name = "plants"
    menu_order = 120
    copy_view_enabled = False
    list_display = ["name", "description"]
    list_per_page = 50
    url_namespace = "plants"
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
        ]),
        MultiFieldPanel([
            FieldPanel("image"),
            FieldPanel("substrate"),
            InlinePanel("notes", label="Notes"),
        ]),
        FieldPanel("copies", classname="collapsed"),
    ]

    def get_queryset(self, request):
        queryset = UserPlant.objects.for_user(request.user)
        return queryset
