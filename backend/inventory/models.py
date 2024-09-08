from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _


class TrainerInventory(models.Model):
    uuid = models.UUIDField(
        default=uuid4,
        editable=False,
        unique=True,
        db_index=True
    )
    trainer = models.ForeignKey(
        'accounts.Trainer',
        on_delete=models.CASCADE,
        related_name='inventories'
    )
    name = models.CharField(
        max_length=25
    )
    description = models.CharField(
        blank=True,
        max_length=255
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


class InventoryPlant(models.Model):
    inventory = models.ForeignKey(
        TrainerInventory,
        on_delete=models.CASCADE,
        related_name='plants'
    )
    plant = models.OneToOneField(
        'biodiversity.Plant',
        on_delete=models.CASCADE,
        related_name='inventory'
    )
    nfc_tag = models.OneToOneField(
        'nearfieldcommunication.NfcTag',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='link'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    last_updated = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Plant: {self.plant.name} -> {self.inventory.name}"

    class Meta:
        unique_together = ('inventory', 'plant', 'nfc_tag')
