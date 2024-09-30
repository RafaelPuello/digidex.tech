BOTANY_PERMISSIONS = [
    'add_plant', 'change_plant', 'delete_plant', 'view_plant',
    'add_inventorybox', 'change_inventorybox', 'delete_inventorybox', 'view_inventorybox'
]


def assign_botany_user_permissions(group):
    from base.utils import assign_group_permissions
    return assign_group_permissions(group, BOTANY_PERMISSIONS)
