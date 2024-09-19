from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission, Group


def setup_ntag_designer_group():
    """
    Creates a group for ntag designers if it does not already exist.
    Then assigns the necessary ntag permissions for the ntag designer group.

    Returns:
        Group: The created or retrieved group instance.
    """
    NTAG_DESIGNER_PERMISSIONS = [
        "view_nfctagdesign",
        "add_nfctagdesign", "change_nfctagdesign", "delete_nfctagdesign",
        "lock_nfctagdesign", "unlock_nfctagdesign",
        "publish_nfctagdesign",
    ]

    group = Group.objects.create("NTAG Designers")
    permissions = Permission.objects.filter(
        codename__in=NTAG_DESIGNER_PERMISSIONS
    )
    group.permissions.add(*permissions)
    group.save()
    return group


def setup_ntag_developer_group():
    """
    Creates a group for ntag developers if it does not already exist.
    Then assigns the necessary ntag permissions for the ntag developer group.

    Returns:
        Group: The created or retrieved group instance.
    """
    NTAG_DEVELOPER_PERMISSIONS = [
        "view_nfctageeprom",
        "add_nfctageeprom", "change_nfctageeprom", "delete_nfctageeprom",
        "lock_nfctageeprom", "unlock_nfctageeprom",
        "publish_nfctageeprom"
    ]

    group = Group.objects.create("NTAG Developers")
    permissions = Permission.objects.filter(
        codename__in=NTAG_DEVELOPER_PERMISSIONS
    )
    group.permissions.add(*permissions)
    group.save()
    return group


def setup_ntag_user_group():
    """
    Creates a group for ntag users if it does not already exist.
    Then assigns the necessary ntag permissions for the ntag user group.

    Returns:
        Group: The created or retrieved group instance.
    """
    NTAG_USER_PERMISSIONS = [
        "view_nfctag", "change_nfctag",
        "view_nfctagdesign",
        "view_nfctagscan",
        "view_nfctageeprom",
    ]

    group = Group.objects.create("NTAG Users")
    permissions = Permission.objects.filter(
        codename__in=NTAG_USER_PERMISSIONS
    )
    group.permissions.add(*permissions)
    group.save()
    return group
