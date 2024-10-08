from wagtail import hooks
from wagtail.snippets.models import register_snippet

from .viewsets import UserPlantViewSet, species_chooser_viewset

@hooks.register("register_icons")
def register_icons(icons):
    return icons + ['botany/icons/plant.svg']


@hooks.register("register_admin_viewset")
def register_species_chooser_viewset():
    return species_chooser_viewset

register_snippet(UserPlantViewSet)  # noqa