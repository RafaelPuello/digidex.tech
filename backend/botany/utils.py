from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission


def assign_botany_permissions(group):
    """
    Assigns the necessary botany permissions for the given group.
    """
    BOTANY_PERMISSIONS = [
        "add_plant",
        "change_plant",
        "delete_plant",
    ]

    permissions = Permission.objects.filter(
        codename__in=BOTANY_PERMISSIONS
    )
    group.permissions.add(*permissions)
    group.save()
    return group
