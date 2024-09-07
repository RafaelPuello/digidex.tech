from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import TrainerInventory

User = get_user_model()

@transaction.atomic
def setup_new_user(instance):
    pass # user_inventory_page = TrainerInventory.create_for_user(instance)
    # instance.set_user_permissions(user_inventory_page)

@receiver(post_save, sender=User)
def new_user_setup(sender, instance, created, **kwargs):
    if created:
        pass # setup_new_user(instance)
