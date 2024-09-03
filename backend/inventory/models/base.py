from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.api import APIField
from wagtail.fields import RichTextField
from wagtail.search import index
from wagtail.models import Page, Collection
from wagtail.admin.panels import FieldPanel


class AbstractInventory(Page):
    uuid = models.UUIDField(
        default=uuid4,
        editable=False,
        unique=True,
        db_index=True
    )
    collection = models.ForeignKey(
        Collection,
        on_delete=models.SET_NULL,
        null=True,
        related_name='+',
    )
    description = models.CharField(
        blank=True,
        max_length=250
    )
    body = RichTextField(
        blank=True
    )

    search_fields = Page.search_fields + [
        index.SearchField('description')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('body'),
    ]

    api_fields = [
        APIField('title'),
        APIField('uuid'),
        APIField('description'),
        APIField('body'),
        APIField('url'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        details = {
            'uuid': self.uuid,
            'name': self.title,
            'description': self.description,
            'body': self.body,
            'url': self.url,
        }

        context.update(details)
        return context

    def create_collection(self, title=None):
        parent_collection = self.get_parent().specific.collection if self.get_parent().specific else None
        if not parent_collection:
            return None
        if not title:
            title = self.title
        try:
            return parent_collection.get_children().get(name=title)
        except Collection.DoesNotExist:
            return parent_collection.add_child(name=title)

    def save(self, *args, **kwargs):
        if not self.collection:
            self.collection = self.create_collection()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['uuid']),
        ]
