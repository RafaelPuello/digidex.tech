from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.models import ClusterableModel


class TrainerInventory(ClusterableModel):
    uuid = models.UUIDField(
        default=uuid4,
        editable=False,
        unique=True,
        db_index=True
    )
    trainer = models.OneToOneField(
        'accounts.Trainer',
        on_delete=models.CASCADE,
        related_name='inventory'
    )
    description = models.CharField(
        blank=True,
        max_length=250
    )

    def generate_prompt(self):
        prompt = f"The trainer's username is {self.trainer.username}:\n"
        if not self.description:
            return prompt
        return f"{prompt}. The trainer's inventory description is: {self.description}"

    def __str__(self):
        return self.trainer.username

    class Meta:
        verbose_name = _("user inventory")
        verbose_name_plural = _("user inventories")
        indexes = [
            models.Index(fields=['uuid']),
        ]
