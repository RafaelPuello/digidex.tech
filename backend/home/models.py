from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class HomePage(Page):
    """
    Represents the homepage of the website.

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

    parent_page_types = [
        'wagtailcore.Page'
    ]
    child_page_types = [
        'inventory.InventoryIndex',
        'blog.BlogIndexPage',
        'blog.TagIndexPage',
        'portfolio.PortfolioIndexPage',
        'contact.ContactFormPage',
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('home page')
        verbose_name_plural = _('home pages')
