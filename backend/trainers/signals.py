from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Trainer, TrainerPage

@transaction.atomic
def setup_new_trainer(instance):
    trainer_page = TrainerPage.create_for_trainer(instance)
    instance.set_trainer_permissions(trainer_page)

@receiver(post_save, sender=Trainer)
def new_trainer_setup(sender, instance, created, **kwargs):
    if created:
        setup_new_trainer(instance)
