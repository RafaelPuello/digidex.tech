import uuid
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from wagtail.models import TranslatableMixin, PreviewableMixin, Orderable
from wagtail.search import index

from base.models import GalleryImageMixin


class UserPlant(
    Orderable,
    ClusterableModel,
    index.Indexed,
    TranslatableMixin,
    PreviewableMixin
):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='plants',
        on_delete=models.CASCADE
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

    search_fields = [
        index.SearchField('name'),
        index.AutocompleteField('name'),
    ]

    def __str__(self):
        return self.name

    class Meta(TranslatableMixin.Meta):
        verbose_name = _('plant')
        verbose_name_plural = _('plants')
        indexes = [
            models.Index(fields=['user', 'name']),
            models.Index(fields=['user', 'slug']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_plant_name_user'),
            models.UniqueConstraint(fields=['user', 'slug'], name='unique_plant_slug_user')
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_preview_template(self, request, mode_name):
        return "botany/user_plant.html"

    @property
    def main_image(self, rendition=None):
        if rendition is None:
            return self.get_main_image()
        pass  # TODO: Implement image rendition

    def get_main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    @property
    def images(self):
        return self.get_images()

    def get_images(self):
        return self.gallery_images.all()

    @property
    def url(self):
        return self.get_url()

    def get_url(self):
        page = self.user.get_page()
        return page.url + self.slug + '/'

    @property
    def collection(self):
        return self.get_parent_collection()

    def get_parent_collection(self):
        return self.user.collection


class UserPlantGalleryImage(GalleryImageMixin):
    plant = ParentalKey(
        UserPlant,
        on_delete=models.CASCADE,
        related_name='gallery_images'
    )

    class Meta(GalleryImageMixin.Meta):
        abstract = False

    def get_image_rendition(self, spec):
        """
        Generates an image rendition based on a given spec string
        (e.g., "fill-300x300").
        """
        return self.image.get_rendition(spec)
