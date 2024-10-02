BOTANY_PERMISSIONS = [
    'add_plant', 'change_plant', 'delete_plant', 'view_plant',
    'add_userboxpage', 'change_userboxpage', 'delete_userboxpage', 'view_userboxpage'
]


def assign_botany_user_permissions(group):
    from base.utils import assign_group_permissions
    return assign_group_permissions(group, BOTANY_PERMISSIONS)

def setup_botany_for_user(user):
    from home.models import UserIndexPage
    user_index_page = UserIndexPage.objects.get_or_create(owner=user)
    