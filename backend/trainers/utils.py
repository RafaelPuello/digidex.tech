from wagtail.models import Collection
from django.core.exceptions import ObjectDoesNotExist

def create_trainer_collection(trainer):
    """
    Creates a collection for the given trainer if it does not already exist.
    The collection path will be: root -> trainer collection -> trainer_[trainer_uuid].
    
    Args:
        trainer (Trainer): An instance of the Trainer model.
        
    Returns:
        Collection: The created or retrieved collection instance.
    """
    # Check if the trainer already has a collection
    if trainer.collection:
        return trainer.collection

    # Get or create the root collection
    try:
        root_collection = Collection.get_first_root_node()
    except ObjectDoesNotExist:
        raise Exception("Root collection not found. Please ensure a root collection exists.")

    # Get or create the 'Trainer Collection' under the root
    trainer_collection = Collection(
        name="Trainer Collections"
    )
    root_collection.add_child(instance=trainer_collection)

    # Create or get the user's specific collection under the 'Trainer Collections'
    user_collection_name = f"trainer_{trainer.uuid}"
    user_collection = Collection(
        name=user_collection_name
    )
    trainer_collection.add_child(instance=user_collection)

    # Assign the collection to the trainer
    trainer.collection = user_collection
    trainer.save()
    return user_collection
