from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.models import Page, Collection
from wagtail.fields import RichTextField
from wagtail.admin.panels import (
    FieldPanel,
    TabbedInterface,
    ObjectList
)


class CompanyIndexPage(Page):
    """
    Represents the company index page.

    Attributes:
        intro (TextField): The introduction of the page.
        body (RichTextField): The body of the page.
    """
    intro = models.TextField(
        blank=True
    )
    body = RichTextField(
        blank=True
    )
    collection = models.ForeignKey(
        Collection,
        null=True,
        on_delete=models.PROTECT,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
        FieldPanel('collection')
    ]

    parent_page_types = [
        'home.HomePage'
    ]

    child_page_types = [
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('company index page')
        verbose_name_plural = _('company index pages')
