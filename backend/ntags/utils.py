from django.db import transaction
from django.contrib.auth.models import Permission, Group

from .constants import GROUPS

def setup_group(name=None, permissions=None):
    """
    Create, setup and return a group for ntag users if it does not already exist.
    """

    group, created = Group.objects.get_or_create(name)
    if created:
        permissions = Permission.objects.filter(codename__in=permissions)
        group.permissions.add(*permissions)
        group.save()
    return group


@transaction.atomic
def setup_app_groups():
    """
    Create and setup groups for ntag users.
    """

    for name, permissions in GROUPS.items():
        setup_group(name, permissions)
