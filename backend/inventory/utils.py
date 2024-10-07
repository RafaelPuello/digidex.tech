from django.db import transaction

from .models import InventoryIndexCollection


@transaction.atomic
def setup_user_inventory(user):
    user.add_to_group("Trainers")
    user_collection = InventoryIndexCollection.get_for_user(user)
    user_collection.get_user_page()  # Make sure the user has an inventory page
