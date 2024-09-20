from uuid import uuid4
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.models import (
    Collection,
    Orderable,
    RevisionMixin,
    DraftStateMixin,
    LockableMixin,
    TranslatableMixin,
    PreviewableMixin
)
from wagtail.fields import RichTextField
from wagtail.images import get_image_model
from wagtail.documents import get_document_model


class Box(
    DraftStateMixin,
    RevisionMixin,
    LockableMixin,
    TranslatableMixin,
    PreviewableMixin,
    Orderable,
    ClusterableModel
):
    """
    Represents an inventory box in the database.

    Attributes:
        owner (ForeignKey): The trainer that owns the inventory box.
        name (str): The name of the inventory box.
        description (str): A description of the inventory box.
        slug (str): A unique slug for the inventory box.
        uuid (uuid): A unique identifier for the inventory box.
        collection (ForeignKey): The collection associated with the inventory box.
    """
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='boxes'
    )
    name = models.CharField(
        max_length=25,
        db_index=True
    )
    description = RichTextField(
        blank=True,
        max_length=255
    )
    slug = models.SlugField(
        max_length=255,
        db_index=True
    )
    uuid = models.UUIDField(
        default=uuid4,
        editable=False,
        unique=True,
        db_index=True
    )
    collection = models.ForeignKey(
        Collection,
        on_delete=models.SET_NULL,
        related_name='+',
        null=True,
        blank=True
    )

    def get_documents(self):
        """
        Returns all documents associated with the inventory box.
        """
        return get_document_model().objects.filter(collection=self.collection)

    def get_images(self):
        """
        Returns all images associated with the inventory box.
        """
        return get_image_model().objects.filter(collection=self.collection)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to generate a slug for the inventory box if one is not provided.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Returns the name of the inventory box.
        """
        return self.name

    class Meta(TranslatableMixin.Meta, Orderable.Meta):
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
        box (ParentalKey): The inventory box the item belongs to.
        content (json): The item contents.
        created_at (datetime): The date and time the item was created.
        last_modified (datetime): The date and time the item was last updated.
    """
    box = ParentalKey(
        Box,
        on_delete=models.CASCADE,
        related_name='items'
    )
    content = models.JSONField(
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    last_modified = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        """
        Returns a string representation of the box item.
        """
        return f"{self.box.name}'s item."

    class Meta:
        verbose_name = _("item")
        verbose_name_plural = _("items")
