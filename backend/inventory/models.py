from uuid import uuid4
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from wagtail.models import Orderable


class Box(Orderable, models.Model):
    """
    Represents an inventory box in the database.

    Attributes:
        owner (ForeignKey): The trainer that owns the inventory.
        name (str): The name of the inventory.
        description (str): A description of the inventory.
        slug (str): A unique slug for the inventory.
        uuid (uuid): A unique identifier for the inventory.
        created_at (datetime): The date and time the inventory was created.
        last_updated (datetime): The date and time the inventory was last updated.
    """

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='inventories'
    )
    name = models.CharField(
        max_length=25,
        db_index=True
    )
    description = models.CharField(
        blank=True,
        max_length=255
    )
    slug = models.SlugField(
        max_length=255,
        unique=True, # Only within constraints specified in the Meta class
        db_index=True
    )
    uuid = models.UUIDField(
        default=uuid4,
        editable=False,
        unique=True,
        db_index=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    last_updated = models.DateTimeField(
        auto_now=True
    )

    def generate_prompt(self):
        prompt = f"The inventory box name is {self.name}"
        if self.description:
            return f"{prompt} and its description is {self.description}"
        return prompt

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("box")
        verbose_name_plural = _("boxes")
        indexes = [
            models.Index(fields=['owner', 'name']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['owner', 'name'], name='unique_owner_inventory')
        ]


class BoxItem(Orderable, models.Model):
    """
    Represents an item in an inventory box in the database.

    Attributes:
        box (ForeignKey): The inventory box the item belongs to.
        nfc_tag (OneToOneField): The NFC tag associated with the item.
        plant (OneToOneField): The plant associated with the item.
        created_at (datetime): The date and time the item was created.
        last_updated (datetime): The date and time the item was last updated.
    """

    box = models.ForeignKey(
        Box,
        on_delete=models.CASCADE,
        related_name='items'
    )
    nfc_tag = models.OneToOneField(
        'nearfieldcommunication.NfcTag',
        on_delete=models.SET_NULL,
        related_name='linked_item',
        null=True
    )
    plant = models.OneToOneField(
        'biodiversity.Plant',
        on_delete=models.SET_NULL,
        related_name='+',
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    last_updated = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.box.name} item."

    class Meta:
        verbose_name = _("box item")
        verbose_name_plural = _("box items")
        constraints = [
            models.UniqueConstraint(fields=['box', 'nfc_tag', 'plant'], name='unique_box_item')
        ]
