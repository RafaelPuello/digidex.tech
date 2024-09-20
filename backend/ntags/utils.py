from django.contrib.auth.models import Permission, Group


def setup_ntag_designer_group():
    """
    Create, setup and return a group for ntag designers if it does not already exist.
    """
    group = Group.objects.create("NTAG Designers")
    permissions = Permission.objects.filter(
        codename__in=[
            "view_nfctagdesign",
            "add_nfctagdesign", "change_nfctagdesign", "delete_nfctagdesign",
            "lock_nfctagdesign", "unlock_nfctagdesign",
            "publish_nfctagdesign",
        ]
    )
    group.permissions.add(*permissions)
    group.save()
    return group


def setup_ntag_developer_group():
    """
    Create, setup and return a group for ntag developers if it does not already exist.
    """
    group = Group.objects.create("NTAG Developers")
    permissions = Permission.objects.filter(
        codename__in=[
            "view_nfctageeprom",
            "add_nfctageeprom", "change_nfctageeprom", "delete_nfctageeprom",
            "lock_nfctageeprom", "unlock_nfctageeprom",
            "publish_nfctageeprom"
        ]
    )
    group.permissions.add(*permissions)
    group.save()
    return group


def setup_ntag_user_group():
    """
    Create, setup and return a group for ntag users if it does not already exist.
    """
    group = Group.objects.create("NTAG Users")
    permissions = Permission.objects.filter(
        codename__in=[
            "view_nfctag", "change_nfctag",
            "view_nfctagdesign",
            "view_nfctagscan",
            "view_nfctageeprom",
        ]
    )
    group.permissions.add(*permissions)
    group.save()
    return group
