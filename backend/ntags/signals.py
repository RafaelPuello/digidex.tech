
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import NFCTagDesign
from .utils import get_collection


@receiver(post_save, sender=NFCTagDesign)
def create_ntag_design_collection(sender, instance, created, **kwargs):
    """
    Signal to create a design-specific collection whenever a new ntag design is created.
    """
    if created:
        try:
            # Get/Create a collection for the app to store all ntag design collections
            app_col = get_collection(name="ntags")

            # Get/Create a collection for the newly created NFCTagDesign instance
            get_collection(parent=app_col, name=str(instance.uuid))
        except Exception as e:
            raise ValueError(f"Error creating Collection for NFCTagDesign {instance}: {e}")
