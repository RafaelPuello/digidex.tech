from wagtail import hooks
from django.contrib.auth.models import Permission
from wagtail.snippets.models import register_snippet

from .viewsets import NfcViewSetGroup


@hooks.register("register_permissions")
def register_permissions():
    app = "nearfieldcommunication"
    model = "nfctagentitylink"

    return Permission.objects.filter(content_type__app_label=app, codename__in=[
        f"view_{model}", f"add_{model}", f"change_{model}", f"delete_{model}"
    ])

register_snippet(NfcViewSetGroup)
