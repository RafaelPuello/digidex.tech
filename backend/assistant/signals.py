from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import TrainerAssistant

Trainer = get_user_model()

@receiver(post_save, sender=Trainer)
def create_trainer_assistant(sender, instance, created, **kwargs):
    """
    Signal to create a trainer-specific assistant whenever a new trainer is created.
    """
    if created:
        try:
            TrainerAssistant.objects.create(trainer=instance)
        except Exception as e:
            raise ValueError(f"Error creating TrainerAssistant for trainer {instance}: {e}")
