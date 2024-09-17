from uuid import uuid4
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class InventoryBox(models.Model):
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


class InventoryPlant(models.Model):
    """
    Represents a plant in a trainer's inventory in the database.

    Attributes:
        inventory (ForeignKey): The inventory that contains the plant.
        plant (ForeignKey): The plant that is in the inventory.
        label (str): A label for the plant in the inventory.
        nfc_tag (ForeignKey): The NFC tag that is linked to the plant in the inventory.
        slug (str): A unique slug for the plant in the inventory.
        uuid (uuid): A unique identifier for the plant in the inventory.
        created_at (datetime): The date and time the plant was added to the inventory.
        last_updated (datetime): The date and time the plant was last updated.
    """
    inventory = models.ForeignKey(
        InventoryBox,
        on_delete=models.CASCADE,
        related_name='plants'
    )
    plant = models.OneToOneField(
        'biodiversity.Plant',
        on_delete=models.CASCADE,
        related_name='inventory'
    )
    label = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    nfc_tag = models.OneToOneField(
        'nearfieldcommunication.NfcTag',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='link'
    )
    uuid = models.UUIDField(
        default=uuid4,
        editable=False,
        unique=True,
        db_index=True
    )
    slug = models.SlugField(
        max_length=255,
        unique=True, # Only within constraints specified in the Meta class
        db_index=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    last_updated = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):
        if not self.slug and self.label:
            self.slug = slugify(self.label)
        super().save(*args, **kwargs)

    def __str__(self):
        if self.label:
            return self.label
        if self.plant:
            return f"Plant: {self.plant.name} -> {self.inventory.name}"
        return f"Inventory: {self.name} with no plant"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['inventory', 'plant', 'nfc_tag'], name='unique_inventory_plant')
        ]
