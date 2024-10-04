from wagtail import hooks
from wagtail.snippets.models import register_snippet

from .views import pokemon_chooser_viewset
from .viewsets import PlantViewSet


@hooks.register("register_icons")
def register_icons(icons):
    return icons + ['botany/icons/plant.svg']

register_snippet(PlantViewSet)


@hooks.register("register_admin_viewset")
def register_pokemon_chooser_viewset():
    return pokemon_chooser_viewset