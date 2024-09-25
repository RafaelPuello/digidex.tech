from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from home.models import UserIndexCollection

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_collection_and_page(sender, instance, created, **kwargs):
    if created:
        # Create the UserIndexCollection for the new user
        user_collection = UserIndexCollection.get_for_user(user=instance)
        
        # Create the UserIndexPage associated with the UserIndexCollection
        user_collection.create_user_page()
