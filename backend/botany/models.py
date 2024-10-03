import uuid
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from wagtail.models import Page, TranslatableMixin, PreviewableMixin, Orderable
from wagtail.fields import RichTextField
from wagtail.search import index
from wagtail.admin.panels import FieldPanel, TabbedInterface, TitleFieldPanel, ObjectList
from wagtail.contrib.routable_page.models import RoutablePageMixin, path

from base.models import GalleryImageMixin


class UserBoxPage(RoutablePageMixin, Page):
    """
    Represents a box page that can contain multiple plants.
    """
    description = RichTextField(
        blank=True
    )
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True
    )

    parent_page_types = [
        'home.UserIndexPage'
    ]
    child_page_types = []

    content_panels = [
        TitleFieldPanel('title', classname="title"),
        FieldPanel('slug'),
        FieldPanel('description'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Details'),
        ObjectList(Page.promote_panels, heading='Promote', permission="superuser"),
        ObjectList(Page.settings_panels, heading='Settings', permission="superuser"),
    ])

    @path('<slug:plant_slug>/')
    def plant_details(self, request, plant_slug):
        plant = get_object_or_404(Plant, slug=plant_slug, box=self)
        return self.render(
            request,
            context_overrides={'plant': plant},
            template="botany/user_plant.html"
        )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['plants'] = self.get_plants()
        return context

    def get_plants(self):
        return Plant.objects.filter(box=self)

    def get_parent_collection(self):
        return self.owner.index_collection.collection

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('box')
        verbose_name_plural = _('boxes')


class Plant(
    Orderable,
    ClusterableModel,
    index.Indexed,
    TranslatableMixin,
    PreviewableMixin
):
    box = models.ForeignKey(
        UserBoxPage,
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
    date = models.DateField(
        null=True,
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
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    last_modified = models.DateTimeField(
        auto_now=True
    )

    search_fields = [
        index.SearchField('name'),
        index.AutocompleteField('name'),
    ]

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
        return self.box.url + self.slug + '/'

    def get_parent_collection(self):
        return self.box.collection

    def get_preview_template(self, request, mode_name):
        return "botany/user_plant.html"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta(TranslatableMixin.Meta):
        verbose_name = _('plant')
        verbose_name_plural = _('plants')
        indexes = [
            models.Index(fields=['box', 'name']),
            models.Index(fields=['box', 'slug']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['box', 'name'], name='unique_plant_name_in_box'),
            models.UniqueConstraint(fields=['box', 'slug'], name='unique_plant_slug_in_box')
        ]


class PlantGalleryImage(GalleryImageMixin):
    plant = ParentalKey(
        Plant,
        on_delete=models.CASCADE,
        related_name='gallery_images'
    )

    class Meta(GalleryImageMixin.Meta):
        abstract = False
