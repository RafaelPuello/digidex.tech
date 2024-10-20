import uuid
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from wagtail.fields import StreamField
from wagtail.models import TranslatableMixin, PreviewableMixin, Orderable
from wagtail.search import index

from base.models import GalleryImageMixin

from .blocks import BotanyNoteBlock
from .forms import UserPlantForm


class UserPlant(
    Orderable,
    ClusterableModel,
    index.Indexed,
    TranslatableMixin,
    PreviewableMixin
):
    box = models.ForeignKey(
        'inventory.InventoryFormPage',
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
        editable=False,
        db_index=True,
        max_length=255
    )
    notes = StreamField(
        [('note', BotanyNoteBlock())],
        blank=True
    )

    search_fields = [
        index.SearchField('name'),
        index.AutocompleteField('name'),
    ]

    base_form_class = UserPlantForm

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta(TranslatableMixin.Meta):
        verbose_name = _('plant')
        verbose_name_plural = _('plants')
        indexes = [
            models.Index(fields=['box', 'name']),
            models.Index(fields=['box', 'slug']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['box', 'name'], name='unique_plant_name_in_box'),
            models.UniqueConstraint(fields=['box', 'slug'], name='unique_plant_slug_in_box'),
        ]

    def get_custom_form_class(self):
        from .forms import UserPlantForm
        return UserPlantForm

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
        return self.box.url + slugify(self.name) + '/'

    @property
    def collection(self):
        return self.get_parent_collection()

    def get_parent_collection(self):
        return self.user.collection

    def get_inventory_form(self, request):
        tasks = {}

        form = self.box.get_form(page=self.box, user=request.user)
        if form:
            tasks.update({
                'form': form,
                # 'form_fields': self.box.get_inventory_form_fields(),
                'form_url': self.box.get_url(request)
            })

        return tasks


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
