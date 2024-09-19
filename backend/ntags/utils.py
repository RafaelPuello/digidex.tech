from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission


def assign_ntag_permissions(group):
    """
    Assigns the necessary ntag permissions for the given group.
    """
    NTAG_PERMISSIONS = [
        "view_nfctag",
        "view_nfctagdesign",
        "view_nfctagscan",
        "view_nfctagmemory",
    ]

    permissions = Permission.objects.filter(
        codename__in=NTAG_PERMISSIONS
    )
    group.permissions.add(*permissions)
    group.save()
    return group
