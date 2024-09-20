import uuid
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from modelcluster.models import ClusterableModel
from wagtail.models import (
    Collection,
    RevisionMixin,
    DraftStateMixin,
    LockableMixin,
    TranslatableMixin,
    PreviewableMixin
)
from wagtail.images import get_image_model
from wagtail.documents import get_document_model


class Plant(
    DraftStateMixin,
    RevisionMixin,
    LockableMixin,
    TranslatableMixin,
    PreviewableMixin,
    ClusterableModel
):
    """
    Represents a plant in the database.

    Attributes:
        owner (ForeignKey): The user who owns the plant.
        name (str): The name of the plant.
        description (str): A description of the plant.
        uuid (uuid): A unique identifier for the plant.
        slug (str): A unique slug for the plant.
        collection (ForeignKey): The collection associated with the plant.
    """
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='plants',
        null=True
    )
    name = models.CharField(
        max_length=255,
        db_index=True
    )
    description = models.TextField(
        blank=True
    )
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True
    )
    slug = models.SlugField(
        max_length=255,
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
        Returns all documents associated with plant.
        """
        return get_document_model().objects.filter(collection=self.collection)

    def get_images(self):
        """
        Returns all images associated with plant.
        """
        return get_image_model().objects.filter(collection=self.collection)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to generate a slug for the plant if one is not provided.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Returns a string representation of the plant.
        """
        return self.name

    class Meta(TranslatableMixin.Meta):
        verbose_name = 'plant'
        verbose_name_plural = 'plants'
        indexes = [
            models.Index(fields=['owner', 'name']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['owner', 'name'], name='unique_owner_plant')
        ]
