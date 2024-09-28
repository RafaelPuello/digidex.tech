from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.models import Page, Collection
from wagtail.fields import StreamField
from wagtail.admin.panels import (
    FieldPanel,
    TabbedInterface,
    ObjectList
)

from .blocks import PortfolioStreamBlock


class CompanyIndexPage(Page):
    """
    Represents the company index page.

    Attributes:
        intro (TextField): The introduction of the page.
        body (RichTextField): The body of the page.
    """

    parent_page_types = ['home.HomePage']
    child_page_types = []

    intro = models.TextField(
        blank=True
    )
    body = StreamField(
        PortfolioStreamBlock(),
        blank=True,
        use_json_field=True,
        help_text="Use this section to list your projects and skills.",
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

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('company index page')
        verbose_name_plural = _('company index pages')
