from .models import UserBoxPage

BOTANY_PERMISSIONS = [
    'add_plant', 'change_plant', 'delete_plant', 'view_plant',
    'add_userboxpage', 'change_userboxpage', 'delete_userboxpage', 'view_userboxpage'
]


def assign_botany_user_permissions(group):
    from base.utils import assign_group_permissions
    return assign_group_permissions(group, BOTANY_PERMISSIONS)


def setup_botany_user(user):
    from home.models import UserIndexPage
    user_index_page = UserIndexPage.get_for_user(user)

    # Create 10 UserBoxPages for the user
    for i in range(1, 11):
        user_box_page = UserBoxPage(
            title=f"Box {i}",
            slug=f"box-{i}",
            owner=user
        )

        user_index_page.add_child(instance=user_box_page)
        user_box_page.save_revision().publish()

    print(f"10 UserBoxPages have been created for user: {user.username}")
