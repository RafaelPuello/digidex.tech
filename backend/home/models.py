from django.utils.translation import gettext_lazy as _
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class HomePage(Page):
    """
    Represents the homepage of the website.
    """

    body = RichTextField(
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('body')
    ]

    parent_page_types = ['wagtailcore.Page']

    child_page_types = ['trainers.TrainerPage']

    def __str__(self):
        """
        Represents the string representation of the homepage by its title.
        """
        return self.title

    class Meta:
        verbose_name = _('homepage')
