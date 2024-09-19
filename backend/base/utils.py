from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission


def assign_base_editor_permissions(group):
    """
    Assigns the necessary base permissions for the given group.
    """
    BASE_PERMISSIONS = [
        "add_image", "change_image", "delete_image",
        "add_document", "change_document", "delete_document",
        "access_admin"
    ]

    permissions = Permission.objects.filter(
        codename__in=BASE_PERMISSIONS
    )
    group.permissions.add(*permissions)
    group.save()
    return group
