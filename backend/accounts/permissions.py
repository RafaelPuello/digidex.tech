from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission


def assign_account_permissions(group):
    """
    Assigns the necessary account permissions for the given group.
    """
    ACCOUNT_PERMISSIONS = [
    ]

    permissions = Permission.objects.filter(
        codename__in=ACCOUNT_PERMISSIONS
    )
    group.permissions.add(*permissions)
    group.save()
    return group
