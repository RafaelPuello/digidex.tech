from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group


def create_home_group(user):
    """
    Creates a group for the user home if it does not already exist.

    Returns:
        Group: The created or retrieved group instance.
    """
    group = Group.objects.create(name=user.uuid)
    user.groups.add(group)
    return group


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
