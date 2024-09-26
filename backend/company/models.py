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
        body (RichTextField): The body of the page.
    """
    body = RichTextField(
        blank=True
    )

    parent_page_types = [
        'home.HomePage'
    ]

    child_page_types = [
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('company page')
        verbose_name_plural = _('company pages')
