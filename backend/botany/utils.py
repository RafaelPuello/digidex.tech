from .models import UserBoxPage

BOTANY_PERMISSIONS = [
    'add_plant', 'change_plant', 'delete_plant', 'view_plant',
    'add_userboxpage', 'change_userboxpage', 'delete_userboxpage', 'view_userboxpage'
]


def assign_botany_user_permissions(group):
    from base.utils import assign_group_permissions
    return assign_group_permissions(group, BOTANY_PERMISSIONS)


def setup_botany_user(user, num_boxes=5):
    from home.models import UserIndexPage
    user_index_page = UserIndexPage.get_for_user(user)

    # Create n UserBoxPages for the user
    for i in range(1, num_boxes+1):
        user_box_page = UserBoxPage(
            title=f"Box {i}",
            slug=f"box-{i}",
            owner=user,
            live=False
        )
        user_index_page.add_child(instance=user_box_page)   
        print(f"Box {i} created.")
    print("Botany user setup complete.")
