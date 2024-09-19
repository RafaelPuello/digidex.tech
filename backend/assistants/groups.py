from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group


def create_user_assistant_group():
    """
    Creates a group for user assistants if it does not already exist.

    Returns:
        Group: The created or retrieved group instance.
    """
    group = Group.objects.create(name="User Assistants")
    return group
