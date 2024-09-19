from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission


def assign_base_permissions(group):
    """
    Assigns the necessary base permissions for the given group.
    """
    BASE_PERMISSIONS = [
    ]

    permissions = Permission.objects.filter(
        codename__in=BASE_PERMISSIONS
    )
    group.permissions.add(*permissions)
    group.save()
    return group
