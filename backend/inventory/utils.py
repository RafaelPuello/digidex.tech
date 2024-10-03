from django.contrib.auth.models import Group

from .models import InventoryIndexPage, InventoryBoxPage

INVENTORY_PERMISSIONS = [
    'add_inventoryboxpage',
    'change_inventoryboxpage',
    'delete_inventoryboxpage',
    'view_inventoryboxpage'
]


def assign_inventory_user_permissions(group):
    from base.utils import assign_group_permissions
    return assign_group_permissions(group, INVENTORY_PERMISSIONS)


def setup_user_inventory(user, num_boxes=5):
    user_index_page = InventoryIndexPage.get_for_user(user)

    # Create n InventoryBoxPage for the user
    for i in range(1, num_boxes+1):
        user_box_page = InventoryBoxPage(
            title=f"Box {i}",
            slug=f"box-{i}",
            owner=user,
            live=False
        )
        user_index_page.add_child(instance=user_box_page)   
        print(f"Box {i} created.")
    print("Inventory user setup complete.")


def get_trainer_group():
    group, created = Group.objects.get_or_create(name="Trainers")
    return group
