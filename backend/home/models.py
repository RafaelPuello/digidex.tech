from django.utils.translation import gettext_lazy as _
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin

from inventory.models import TrainerInventory


class HomePage(RoutablePageMixin, Page):
    body = RichTextField(
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('body')
    ]

    parent_page_types = ['wagtailcore.Page']

    child_page_types = []

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('homepage')


class TrainerPage(Page):
    body = RichTextField(
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('body')
    ]

    parent_page_types = ['home.HomePage']

    child_page_types = []

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('trainer page')
        verbose_name_plural = _('trainer pages')
