from wagtail import hooks
from wagtail.snippets.models import register_snippet
from django.templatetags.static import static
from django.utils.html import format_html

from .viewsets import NFCTagSnippetViewSetGroup


@hooks.register("insert_editor_js")
def editor_js():
    return format_html('<script src="{}"></script>', static("ntags/js/nfc-tag-editor.js"))


@hooks.register("register_icons")
def register_icons(icons):
    return icons + [
        'ntags/icons/logo.svg',
        'ntags/icons/designs.svg',
        'ntags/icons/scans.svg',
        'ntags/icons/memory.svg',
    ]


register_snippet(NFCTagSnippetViewSetGroup)  # noqa