from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from home.models import UserIndexCollection

User = get_user_model()

def user_setup(user):
    user_collection = UserIndexCollection.get_for_user(user)
    user_collection.create_user_page()


@receiver(post_save, sender=User)
def create_user_collection_and_page(sender, instance, created, **kwargs):
    if created:
        user_setup(instance)
    