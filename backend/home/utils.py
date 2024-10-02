from django.contrib.auth.models import Group


def get_trainer_group():
    """
    Creates a group for the Trainers if it does not already exist.

    Returns:
        Group: The created or retrieved group instance.
    """
    group, created = Group.objects.get_or_create(name="Trainers")
    return group

def get_page_for_user(user):
    """
    Returns the user's home page.

    Args:
        user (User): The user whose home page is to be retrieved.

    Returns:
        UserIndexPage: The user's home page.
    """
    from home.models import UserIndexPage
    return UserIndexPage.objects.get_or_create(owner=user)