from django.db import transaction
from django.contrib.auth.models import Permission, Group
from wagtail.models import Collection

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


def get_root_collection():
    root_col = Collection.get_first_root_node()
    if not root_col:
        raise Exception("Root collection not found. Please ensure a root collection exists.")
    return root_col


def get_collection(parent=None, name="ntags"):
    if parent is None:
        parent = Collection.get_first_root_node()
    try:
        return parent.get_children().get(name=name)
    except Collection.DoesNotExist:
        return parent.add_child(instance=Collection(name=name))
