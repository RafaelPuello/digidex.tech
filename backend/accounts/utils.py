from django.contrib.auth.models import Group


def create_user_group(user):
    """
    Creates a group for the user if it does not already exist.

    Returns:
        Group: The created or retrieved group instance.
    """

    group = Group.objects.create(name=user.uuid)
    user.groups.add(group)
    return group
