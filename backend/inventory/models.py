from uuid import uuid4
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.models import (
    Orderable,
    RevisionMixin,
    DraftStateMixin,
    LockableMixin,
    TranslatableMixin,
    PreviewableMixin
)
from wagtail.fields import RichTextField


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
        owner (ForeignKey): The trainer that owns the inventory.
        name (str): The name of the inventory.
        description (str): A description of the inventory.
        slug (str): A unique slug for the inventory.
        uuid (uuid): A unique identifier for the inventory.
        created_at (datetime): The date and time the inventory was created.
        last_modified (datetime): The date and time the inventory was last updated.
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
    description = RichTextField(
        blank=True,
        max_length=255
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,  # Only within constraints specified in the Meta class
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
    last_modified = models.DateTimeField(
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
        limit (Q): The limit for the content_type field to restrict the choices to specific models.
        content_type (ForeignKey): The content type of the item.
        object_id (int): The ID of the item.
        content_object (GenericForeignKey): The item itself.
        created_at (datetime): The date and time the item was created.
        last_modified (datetime): The date and time the item was last updated.
    """

    box = ParentalKey(
        Box,
        on_delete=models.CASCADE,
        related_name='items'
    )
    limit = models.Q(
        app_label='biodiversity',
        model='Plant'
    )
    content_type = models.ForeignKey(
        ContentType,
        limit_choices_to=limit,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        db_index=True
    )
    content_object = GenericForeignKey(
        'content_type',
        'object_id'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    last_modified = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.box.name} item."

    class Meta(Orderable.Meta):
        verbose_name = _("box item")
        verbose_name_plural = _("box items")
        constraints = [
            models.UniqueConstraint(fields=["box", "content_type", "object_id"], name='unique_box_item')
        ]
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
