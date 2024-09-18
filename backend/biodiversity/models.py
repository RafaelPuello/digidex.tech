from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
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
        name (str): The name of the plant.
        description (str): A description of the plant.
        collection (ForeignKey): The collection associated with the plant.
    """
    name = models.CharField(
        max_length=255,
        db_index=True
    )
    description = models.TextField(
        blank=True
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

    def __str__(self):
        """
        Returns a string representation of the plant.
        """
        return self.name

    class Meta(TranslatableMixin.Meta):
        verbose_name = 'plant'
        verbose_name_plural = 'plants'
