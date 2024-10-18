from base.blocks import BaseCardBlock, ImageChooserBlock
from django.utils.translation import gettext_lazy as _


class BotanyNoteBlock(BaseCardBlock):
    image = ImageChooserBlock(required=False)
    class Meta:
        label = _("note")
