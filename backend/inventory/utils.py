import uuid
from django.db.models import QuerySet

from .models import UserInventory, Entity

def get_inventory_index(user_inventory_uuid: uuid) -> QuerySet[Entity]:
    """
    Retrieves all entities associated with a user's inventory.
    
    Args:
        user_inventory_uuid: The UUID of the user's inventory (A wagtail page subclass).
    
    Returns:
        A list of entities associated with the user's inventory.
    """
    try:
        user_inventory = UserInventory.objects.get(uuid=user_inventory_uuid)
        return user_inventory.get_entities()
    except UserInventory.DoesNotExist:
        return Entity.objects.none() 

def get_inventory_detail(entity_uuid: uuid) -> Entity:
    """
    Retrieves the featured entity associated with a user inventory.
    
    Args:
        entity_uuid: The UUID of the entity.
    
    Returns:
        A list of entities associated with the entity.
    """
    try:
        return Entity.objects.get(uuid=entity_uuid)
    except Entity.DoesNotExist:
        return Entity.objects.none()
