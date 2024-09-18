from django.db import models
from django.utils.translation import gettext_lazy as _
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
from wagtail.images import get_image_model_string


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
        created_at (datetime): The date and time the plant was created.
        last_modified (datetime): The date and time the plant was last updated.
    """
    name = models.CharField(
        max_length=255,
        db_index=True
    )
    description = models.TextField(
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    last_modified = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name

    class Meta(TranslatableMixin.Meta):
        verbose_name = 'plant'
        verbose_name_plural = 'plants'


class PlantGalleryImage(Orderable):
    """
    Model representing an image associated with a plant.

    Attributes:
        plant (Plant): The plant associated with the image.
        image (Image): The image file.
        caption (str): A caption for the image.
    """

    plant = ParentalKey(
        Plant,
        on_delete=models.CASCADE,
        related_name='gallery_images'
    )
    image = models.ForeignKey(
        get_image_model_string(),
        on_delete=models.CASCADE,
        related_name='+'
    )
    caption = models.CharField(
        blank=True,
        max_length=250
    )

    def __str__(self):
        """
        Returns a string representation of the plant image.
        """
        return f"{self.plant.name} image #{self.sort_order}"

    class Meta:
        verbose_name = _("plant image")
        verbose_name_plural = _("plant images")
