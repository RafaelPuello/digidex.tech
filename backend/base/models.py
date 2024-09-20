from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.models import Orderable
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtail.documents.models import Document, AbstractDocument


class BaseDocument(Orderable, AbstractDocument):
    """
    A model to store a document with additional fields.
    """
    source = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    caption = models.CharField(
        blank=True,
        max_length=250
    )

    admin_form_fields = Document.admin_form_fields + (
        'source',
        'caption'
    )


class BaseImage(Orderable, AbstractImage):
    """
    A model to store an image with additional fields.
    """
    alt = models.CharField(
        blank=True,
        null=True,
        max_length=75
    )
    caption = models.CharField(
        blank=True,
        max_length=250
    )

    admin_form_fields = Image.admin_form_fields + (
        'alt',
        'caption'
    )


class BaseRendition(AbstractRendition):
    """
    A model to store an image rendition with additional fields.
    """
    image = models.ForeignKey(
        BaseImage,
        on_delete=models.CASCADE,
        related_name='renditions'
    )

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )
