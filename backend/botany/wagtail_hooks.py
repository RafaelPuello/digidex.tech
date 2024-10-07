from wagtail import hooks
from wagtail.admin.viewsets.chooser import ChooserViewSet
from wagtail.admin.panels import TabbedInterface, FieldPanel, InlinePanel, ObjectList
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import PlantSpecies, UserPlant


@hooks.register("register_icons")
def register_icons(icons):
    return icons + ['botany/icons/plant.svg']


class PlantSpeciesChooserViewSet(ChooserViewSet):
    model = PlantSpecies
    choose_one_text = "Choose a plant"


@hooks.register("register_admin_viewset")
def register_plant_species_chooser_viewset():
    return PlantSpeciesChooserViewSet("plant_species")


class UserPlantSnippetViewSet(SnippetViewSet):
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

    public_panels = [
        FieldPanel("user"),
        FieldPanel("name"),
        FieldPanel("description"),
        InlinePanel("gallery_images", label="Images"),
    ]

    private_panels = [
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(public_panels, heading='Details'),
            ObjectList(private_panels, heading='Admin only', permission="superuser"),
        ]
    )

    def get_queryset(self, request):
        queryset = UserPlant.objects.filter(user=request.user)
        return queryset


register_snippet(UserPlantSnippetViewSet)
