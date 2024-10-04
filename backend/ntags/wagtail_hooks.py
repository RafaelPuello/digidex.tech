from django.templatetags.static import static
from django.utils.html import format_html
from wagtail import hooks
from wagtail.snippets.models import register_snippet

from .viewsets import NFCTagSnippetViewSet


@hooks.register("register_icons")
def register_icons(icons):
    return icons + [
        'ntags/icons/nfc-icon.svg',
        'ntags/icons/nfc-types.svg',
    ]


@hooks.register("insert_editor_js")
def editor_js():
    return format_html('<script src="{}"></script>', static("base/js/page-editor.js"))


register_snippet(NFCTagSnippetViewSet)