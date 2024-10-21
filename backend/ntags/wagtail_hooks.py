from wagtail import hooks
from wagtail.snippets.models import register_snippet

from .viewsets import NFCTagSnippetViewSet


@hooks.register("register_icons")
def register_icons(icons):
    return icons + [
        'nfctags/icons/logo.svg',
        'nfctags/icons/scans.svg',
    ]


register_snippet(NFCTagSnippetViewSet)  # noqa