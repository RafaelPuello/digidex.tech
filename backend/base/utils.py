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


def assign_wagtail_group_permissions(group, obj, permissions):
    from wagtail.models import Page, GroupPagePermission, Collection, GroupCollectionPermission

    if isinstance(obj, Page):
        for perm in permissions:
            permission = Permission.objects.get(codename=perm)
            
            if not GroupPagePermission.objects.filter(
                    group=group,
                    page=obj,
                    permission=permission
                ).exists():
                GroupPagePermission.objects.create(
                    group=group,
                    page=obj,
                    permission=permission
                )
        return
    elif isinstance(obj, Collection):
        for perm in permissions:
            permission = Permission.objects.get(codename=perm)

            if not GroupCollectionPermission.objects.filter(
                    group=group,
                    collection=obj,
                    permission=permission
                ).exists():
                GroupCollectionPermission.objects.create(
                    group=group,
                    collection=obj,
                    permission=permission
                )
        return
