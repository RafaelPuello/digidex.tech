from datetime import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.api import APIField
from wagtail.images import get_image_model
from wagtail.models import Orderable
from wagtail.admin.panels import FieldPanel, InlinePanel

from nearfieldcommunication.models import NfcTag
from .base import AbstractInventory

Image = get_image_model()


class Entity(AbstractInventory):
    nfc_tag = models.OneToOneField(
        NfcTag,
        on_delete=models.SET_NULL,
        null=True,
        related_name='linked_entity',
    )

    parent_page_types = ['inventory.UserInventory']

    subpage_types = []
    
    content_panels = AbstractInventory.content_panels + [
        FieldPanel('nfc_tag'),
        InlinePanel('gallery_images', label="Gallery Images"),
    ]

    api_fields = AbstractInventory.api_fields + [
        APIField('gallery_images'),
    ]

    template = 'inventory/inventory_entity.html'

    def get_context(self, request):
        context = super().get_context(request)
        context['main_image'] = self.get_main_image().image if self.get_main_image() else None
        context['date'] = self.get_date()
        return context          

    def get_main_image(self):
        return self.gallery_images.select_related('image').first() if self.gallery_images.exists() else None

    def get_date(self):
        return self.first_published_at.strftime('%d/%m/%Y') if self.first_published_at else datetime.today().strftime('%d/%m/%Y')

    def generate_prompt(self):
        images = self.gallery_images()
        prompt = f"The object's name is {self.title} and it currently has {len(images)} image(s)"
        if not self.description:
            return prompt
        return f"{prompt}. The object's description is: {self.description}"

    class Meta:
        verbose_name = _("entity")
        verbose_name_plural = _("entities")


class EntityGalleryImage(Orderable):
    entity = ParentalKey(
        Entity,
        related_name='gallery_images'
    )
    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        related_name='+'
    )
    caption = models.CharField(
        blank=True,
        max_length=250
    )

    panels = [
        FieldPanel('image'),
        FieldPanel('caption')
    ]
