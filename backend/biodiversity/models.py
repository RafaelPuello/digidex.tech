from django.db import models
from django.utils.translation import gettext_lazy as _


class Plant(models.Model):
    """
    Represents a plant in the database.

    Attributes:
        name (str): The name of the plant.
        description (str): A description of the plant.
        nfc_tag (NFCTag): The NFC tag associated with the plant.
        created_at (datetime): The date and time the plant was created.
        updated_at (datetime): The date and time the plant was last updated.
    """
    name = models.CharField(
        max_length=255,
        db_index=True
    )
    description = models.TextField(
        blank=True
    )
    nfc_tag = models.OneToOneField(
        'nearfieldcommunication.NFCTag',
        null=True,
        on_delete=models.SET_NULL,
        related_name='linked_plant'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('plant')
        verbose_name_plural = _('plants')
