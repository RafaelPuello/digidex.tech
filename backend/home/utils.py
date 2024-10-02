from django.contrib.auth.models import Group


def get_trainer_group():
    """
    Creates a group for the Trainers if it does not already exist.

    Returns:
        Group: The created or retrieved group instance.
    """
    group, created = Group.objects.get_or_create(name="Trainers")
    return group
