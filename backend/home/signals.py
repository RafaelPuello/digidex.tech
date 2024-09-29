from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .utils import get_trainer_group
from .models import UserIndexCollection

User = get_user_model()

@transaction.atomic
def user_setup(user):
    group = get_trainer_group()
    user.groups.add(group)

    user_collection = UserIndexCollection.get_for_user(user)
    user_collection.set_permissions()

    user_page = user_collection.create_user_page()
    user_page.set_permissions()
    return


@receiver(post_save, sender=User)
def create_user_collection_and_page(sender, instance, created, **kwargs):
    if created:
        user_setup(instance)
    