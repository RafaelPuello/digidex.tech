from wagtail import hooks
from wagtail.snippets.models import register_snippet
from django.templatetags.static import static
from django.utils.html import format_html

from .viewsets import NFCTagSnippetViewSetGroup


@hooks.register("insert_editor_js")
def editor_js():
    return format_html('<script src="{}"></script>', static("nfctags/js/nfc-tag-editor.js"))


@hooks.register("register_icons")
def register_icons(icons):
    return icons + [
        'nfctags/icons/logo.svg',
        'nfctags/icons/designs.svg',
        'nfctags/icons/scans.svg',
        'nfctags/icons/memory.svg',
    ]


register_snippet(NFCTagSnippetViewSetGroup)  # noqa