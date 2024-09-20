from django.db import transaction
from django.contrib.auth.models import Permission, Group

# Roles
DESIGNERS = "NTAG Designers"
DESIGNER_PERMISSIONS = [
    "view_nfctagdesign",
    "add_nfctagdesign", "change_nfctagdesign", "delete_nfctagdesign",
    "lock_nfctagdesign", "unlock_nfctagdesign",
    "publish_nfctagdesign",
]

DEVELOPERS = "NTAG Developers"
DEVELOPER_PERMISSIONS = [
    "view_nfctageeprom",
    "add_nfctageeprom", "change_nfctageeprom", "delete_nfctageeprom",
    "lock_nfctageeprom", "unlock_nfctageeprom",
    "publish_nfctageeprom"
]

USERS = "NTAG Users"
USER_PERMISSIONS = [
    "view_nfctag", "change_nfctag",
    "view_nfctagdesign",
    "view_nfctagscan",
    "view_nfctageeprom",
]

GROUPS = {
    DESIGNERS: DESIGNER_PERMISSIONS,
    DEVELOPERS: DEVELOPER_PERMISSIONS,
    USERS: USER_PERMISSIONS
}

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
