from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import UserAssistant

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_assistant(sender, instance, created, **kwargs):
    """
    Signal to create a user-specific assistant whenever a new user is created.
    """
    if created:
        try:
            UserAssistant.objects.create(user=instance)
        except Exception as e:
            raise ValueError(f"Error creating UserAssistant for user {instance}: {e}")
