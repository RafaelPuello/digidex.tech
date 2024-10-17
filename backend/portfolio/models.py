from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel


class PortfolioIndexPage(Page):
    """
    Represents the portfolio index page.

    Attributes:
        intro (TextField): The introduction of the page.
    """
    intro = models.TextField(
        blank=True
    )

    parent_page_types = [
        'home.HomePage'
    ]
    child_page_types = []

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('portfolio index page')
        verbose_name_plural = _('portfolio index pages')
