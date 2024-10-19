from wagtail import hooks
from wagtail.snippets.models import register_snippet

from .viewsets import UserPlantViewSet

@hooks.register("register_icons")
def register_icons(icons):
    return icons + ['botany/icons/plant.svg']


register_snippet(UserPlantViewSet)  # noqa