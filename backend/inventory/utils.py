from django.db import transaction

from .models import InventoryBox


@transaction.atomic
def setup_user_inventory(user, num_boxes=5):
    user_inventory = user.get_page()

    for i in range(1, num_boxes + 1):
        user_box_page = InventoryBox(
            title=f"Box {i}",
            slug=f"box-{i}",
            owner=user_inventory.owner
        )
        try:
            user_inventory.add_child(instance=user_box_page)
        except Exception as e:
            print(e)
            continue
