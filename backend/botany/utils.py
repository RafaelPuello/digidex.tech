BOTANY_PERMISSIONS = [
    'add_plant', 'change_plant', 'delete_plant', 'view_plant'
]


def assign_botany_user_permissions(group):
    from base.utils import assign_group_permissions
    return assign_group_permissions(group, BOTANY_PERMISSIONS)
