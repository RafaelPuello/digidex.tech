from django.contrib.auth.models import Permission


def assign_group_permissions(group, permissions):
    """
    Assigns the passed permissions for the given group.
    """
    _permissions = Permission.objects.filter(
        codename__in=permissions
    )
    group.permissions.add(*_permissions)
    group.save()
    return group
