from wagtail.admin.panels import TabbedInterface, FieldPanel, FieldRowPanel, InlinePanel, ObjectList
from wagtail.snippets.views.chooser import SnippetChooserViewSet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import UserPlant


class UserPlantChooserViewSet(SnippetChooserViewSet):
    model = UserPlant
    icon = "plant"
    choose_one_text = "Choose a plant"
    edit_item_text = "Edit this plant"
    form_fields = ["name", "description"]

    def __init__(self, *args, **kwargs):
        # import requests
        # from django.conf import settings
        # r = requests.get(f"{settings.WAGTAILADMIN_BASE_URL}/api/users/")
        # r.raise_for_status()
        # results = r.json()
        # return results
        super().__init__(*args, **kwargs)


class UserPlantViewSet(SnippetViewSet):
    model = UserPlant
    icon = "plant"
    menu_label = "Plants"
    menu_name = "plants"
    menu_order = 120
    copy_view_enabled = True
    admin_url_namespace = "inventory_plants"
    list_display = ["name", "description"]
    list_per_page = 50
    admin_url_namespace = "plants"
    base_url_path = "inventory/plants"
    add_to_admin_menu = True
    chooser_viewset_class = UserPlantChooserViewSet

    detail_panels = [
        FieldRowPanel([
            FieldPanel("box"),
            FieldPanel("name"),
        ]),
        FieldPanel("description"),
    ]

    journal_panels = [
        FieldPanel("notes", classname="collapsed"),
        InlinePanel("gallery_images", label="Image Gallery", classname="collapsed"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(detail_panels, heading='Details'),
            ObjectList(journal_panels, heading='Journal'),
        ]
    )

    def get_queryset(self, request):
        queryset = UserPlant.objects.filter(box__owner=request.user)
        return queryset
