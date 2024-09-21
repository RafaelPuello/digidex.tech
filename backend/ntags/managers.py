from django.db import models
from django.contrib.contenttypes.models import ContentType

from .models import NFCTaggedItem, NFCTag


class NFCTagManager(models.Manager):
    def __init__(self, through=None, model=None, instance=None):
        self.through = through
        self.model = model
        self.instance = instance
        super().__init__()

    def __get__(self, instance, model):
        manager = NFCTagManager(
            through=self.through,
            model=self.model,
            instance=instance
        )
        return manager

    def add(self, *tags):
        for tag in tags:
            NFCTaggedItem.objects.create(
                nfc_tag=tag,
                content_object=self.instance
            )

    def remove(self, *tags):
        NFCTaggedItem.objects.filter(
            nfc_tag__in=tags,
            content_type=ContentType.objects.get_for_model(self.instance),
            object_id=self.instance.pk
        ).delete()

    def clear(self):
        NFCTaggedItem.objects.filter(
            content_type=ContentType.objects.get_for_model(self.instance),
            object_id=self.instance.pk
        ).delete()

    def all(self):
        return NFCTag.objects.filter(
            tagged_items__content_type=ContentType.objects.get_for_model(self.instance),
            tagged_items__object_id=self.instance.pk
        )
