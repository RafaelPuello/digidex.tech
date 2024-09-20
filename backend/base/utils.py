from django.contrib.auth.models import Permission


def assign_base_editor_permissions(group):
    """
    Assigns the necessary base permissions for the given group.
    """
    permissions = Permission.objects.filter(
        codename__in=[
            "add_image", "change_image", "delete_image",
            "add_document", "change_document", "delete_document",
            "access_admin"
        ]
    )
    group.permissions.add(*permissions)
    group.save()
    return group
