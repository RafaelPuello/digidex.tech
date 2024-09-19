from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission


def assign_assistant_permissions(group):
    """
    Assigns the necessary assistant permissions for the given group.
    """
    ASSISTANT_PERMISSIONS = [
    ]

    permissions = Permission.objects.filter(
        codename__in=ASSISTANT_PERMISSIONS
    )
    group.permissions.add(*permissions)
    group.save()
    return group
