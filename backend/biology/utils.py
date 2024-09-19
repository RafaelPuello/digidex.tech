from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission


def assign_biology_permissions(group):
    """
    Assigns the necessary biology permissions for the given group.
    """
    BIOLOGY_PERMISSIONS = [
        "add_plant",
        "change_plant",
        "delete_plant",
    ]

    permissions = Permission.objects.filter(
        codename__in=BIOLOGY_PERMISSIONS
    )
    group.permissions.add(*permissions)
    group.save()
    return group
