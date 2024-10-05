NTAG_USERS_PERMISSIONS = [
    'change_nfctag', 'view_nfctag',
    'view_nfctageeprom',
    'view_nfctagscan'
]


def assign_ntag_user_permissions(group):
    from base.utils import assign_group_permissions
    return assign_group_permissions(group, NTAG_USERS_PERMISSIONS)
