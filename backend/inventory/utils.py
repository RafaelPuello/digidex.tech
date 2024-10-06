from django.db import transaction

from .models import InventoryIndexCollection, InventoryBoxPage


@transaction.atomic
def setup_user_inventory(user):
    user.add_to_group("Trainers")
    user_collection = InventoryIndexCollection.get_for_user(user)
    user_inventory = user_collection.get_user_page()
    setup_inventory_boxes(user_inventory)


def setup_inventory_boxes(user_inventory, num_boxes=5):
    for i in range(1, num_boxes + 1):
        user_box_page = InventoryBoxPage(
            title=f"Box {i}",
            slug=f"box-{i}",
            owner=user_inventory.owner
        )
        try:
            user_inventory.add_child(instance=user_box_page)
        except Exception as e:
            print(e)
            continue
