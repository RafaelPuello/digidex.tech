from wagtail import hooks
from wagtail.snippets.models import register_snippet

from .viewsets import PlantViewSet, plant_species_chooser_viewset


@hooks.register("register_icons")
def register_icons(icons):
    return icons + ['botany/icons/plant.svg']


register_snippet(PlantViewSet)


@hooks.register("register_admin_viewset")
def register_plant_species_chooser_viewset():
    return plant_species_chooser_viewset
