from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .utils import setup_user_inventory

User = get_user_model()


@receiver(post_save, sender=User)
def user_setup(sender, instance, created, **kwargs):
    if created:
        setup_user_inventory(instance)
