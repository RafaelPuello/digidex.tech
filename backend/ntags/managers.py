from django.db import models
from django.utils.translation import gettext_lazy as _


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
