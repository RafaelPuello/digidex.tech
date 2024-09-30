import uuid
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from wagtail.models import Page, TranslatableMixin, PreviewableMixin, Orderable
from wagtail.fields import RichTextField
from wagtail.images import get_image_model
from wagtail.documents import get_document_model
from wagtail.search import index
from wagtail.admin.panels import FieldPanel

from base.models import CollectionMixin


class InventoryBox(CollectionMixin, Page):
    """
    Represents an inventory box that can contain multiple plants.
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

    content_panels = Page.content_panels + [
        FieldPanel('description'),
    ]

    def get_context(self, request, *args, **kwargs):
        context =  super().get_context(request, *args, **kwargs)
        context['plants'] = self.get_plants()
        return context

    def get_plants(self):
        return Plant.objects.filter(box=self)

    def get_documents(self):
        return get_document_model().objects.filter(collection=self.collection)

    def get_images(self):
        return get_image_model().objects.filter(collection=self.collection)

    def get_parent_collection(self):
        return self.owner.index_collection.collection

    def get_collection(self):
        parent_collection = self.get_parent_collection()
        return self.get_or_create_collection(name=self.uuid, parent=parent_collection)

    def save(self, *args, **kwargs):
        if not self.collection:
            self.collection = self.get_collection()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('box')
        verbose_name_plural = _('boxes')


class Plant(
    Orderable,
    CollectionMixin,
    index.Indexed,
    TranslatableMixin,
    PreviewableMixin,
    models.Model
):
    box = models.ForeignKey(
        InventoryBox,
        related_name='plants',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=255,
        db_index=True
    )
    description = RichTextField(
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

    def get_parent_collection(self):
        return self.box.collection

    def get_collection(self):
        parent_collection = self.get_parent_collection()
        return self.get_or_create_collection(name=self.uuid, parent=parent_collection)

    def get_documents(self):
        return get_document_model().objects.filter(collection=self.collection)

    def get_images(self):
        return get_image_model().objects.filter(collection=self.collection)

    def get_preview_template(self, request, mode_name):
        return "botany/inventory_plant.html"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.collection:
            self.collection = self.get_collection()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta(TranslatableMixin.Meta):
        verbose_name = _('plant')
        verbose_name_plural = _('plants')
        indexes = [
            models.Index(fields=['box', 'name']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['box', 'name'], name='unique_plant_name_in_box')
        ]
