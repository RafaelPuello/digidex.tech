from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.fields import RichTextField
from wagtail.models import DraftStateMixin, PreviewableMixin, RevisionMixin, TranslatableMixin
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting


class BaseImage(AbstractImage):
    alt = models.CharField(
        blank=True,
        null=True,
        max_length=75
    )
    caption = models.CharField(
        blank=True,
        max_length=250
    )

    admin_form_fields = Image.admin_form_fields + (
        'alt',
        'caption'
    )


class BaseRendition(AbstractRendition):
    image = models.ForeignKey(
        BaseImage,
        on_delete=models.CASCADE,
        related_name='renditions'
    )

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )


@register_setting
class NavigationSettings(BaseGenericSetting):
    logo = models.ForeignKey(
        BaseImage,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='+'
    )
    github_url = models.URLField(
        verbose_name="GitHub URL",
        blank=True,
        null=True
    )

    panels = [
        FieldPanel("logo"),
        FieldPanel("github_url"),
    ]


class FooterSection(DraftStateMixin, RevisionMixin, PreviewableMixin, TranslatableMixin, models.Model):
    body = RichTextField(
        max_length=100
    )
    copyright = models.TextField(
        max_length=100
    )

    def __str__(self):
        return f"Footer Body - {self.id}"

    def get_preview_template(self, request, mode_name):
        return "base.html"

    def get_preview_context(self, request, mode_name):
        return {
            "body": self.body,
            "copyright": self.copyright
        }

    class Meta(TranslatableMixin.Meta):
        verbose_name = _("Footer Body")
        verbose_name_plural = _("Footer Bodies")
