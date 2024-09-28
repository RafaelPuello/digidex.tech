from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel
)
from wagtail.fields import RichTextField
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.panels import FormSubmissionsPanel


class ContactFormField(AbstractFormField):
    page = ParentalKey(
        'support.ContactFormPage',
        on_delete=models.CASCADE,
        related_name='form_fields'
    )


class ContactFormPage(AbstractEmailForm):
    intro = RichTextField(
        blank=True
    )
    thank_you_text = RichTextField(
        blank=True
    )

    parent_page_types = [
        'home.HomePage'
    ]
    child_page_types = []

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('intro'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address'),
                FieldPanel('to_address'),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]
