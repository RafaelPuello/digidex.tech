from django.db import transaction
from django.contrib.auth.models import Group

from base.utils import assign_group_permissions, assign_wagtail_group_permissions

NTAG_PERMISSIONS = (
    'change_nfctag', 'view_nfctagdesign', 'view_nfctagscan'
)

BOTANY_PERMISSIONS = (
    'add_plant', 'change_plant', 'delete_plant', 'view_plant'
)

COLLECTION_PERMISSIONS = (
    'add_image', 'change_image', 'choose_image',
    'add_document', 'change_document', 'choose_document'
)

PAGE_PERMISSIONS = (
    'add_page', 'publish_page'
)


@transaction.atomic
def setup_new_trainer(user):
    # Assign user permissions
    assign_user_permissions(user)
    # Assign trainer permissions
    assign_trainer_permissions(user)
    # Setup inventory boxes for the new user
    from inventory.utils import setup_inventory_boxes
    setup_inventory_boxes(user)


def assign_user_permissions(user):

    assign_trainer_permissions(user)
    group = user.get_group()

    collection = user.get_collection()
    assign_wagtail_group_permissions(group, collection, COLLECTION_PERMISSIONS)

    page = user.get_page()
    assign_wagtail_group_permissions(group, page, PAGE_PERMISSIONS)


def assign_trainer_permissions(user):

    group, created = Group.objects.get_or_create(name='Trainers')
    if created:
        # Assign botany permissions for all trainers
        assign_group_permissions(group, BOTANY_PERMISSIONS)

        # Assign ntag permissions for all trainers
        assign_group_permissions(group, NTAG_PERMISSIONS)
    user.groups.add(group)
