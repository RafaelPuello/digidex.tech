from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver

from .utils import setup_new_trainer

User = settings.AUTH_USER_MODEL

@receiver(post_save, sender=User)
def new_user_setup(sender, instance, created, **kwargs):
    if created:
        setup_new_trainer(instance)
