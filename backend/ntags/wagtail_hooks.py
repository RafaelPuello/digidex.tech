from wagtail import hooks
from wagtail.snippets.models import register_snippet

from .viewsets import NFCTagSnippetViewSet


@hooks.register("register_icons")
def register_icons(icons):
    return icons + [
        'ntags/icons/nfc-icon.svg',
        'ntags/icons/nfc-types.svg',
    ]


register_snippet(NFCTagSnippetViewSet)