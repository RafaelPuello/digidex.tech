from wagtail.blocks import (
    CharBlock,
    TextBlock,
    ChoiceBlock,
    DateBlock,
    RichTextBlock,
    StructBlock
)
from wagtail.images.blocks import ImageChooserBlock


class BaseHeadingBlock(StructBlock):
    heading_value = CharBlock(form_classname="title")
    size = ChoiceBlock(
        choices=[
            ("", "Select a heading size"),
            ("h2", "H2"),
            ("h3", "H3"),
        ],
        blank=True,
        required=False,
    )

    class Meta:
        icon = "title"
        template = "base/blocks/base_heading_block.html"


class BaseImageBlock(StructBlock):
    image = ImageChooserBlock()
    caption = CharBlock(required=False)
    attribution = CharBlock(required=False)

    class Meta:
        icon = "image"
        template = "base/blocks/base_image_block.html"


class BaseBodyBlock(RichTextBlock):
    features = [
        'h4', 'h5', 'bold', 'italic', 'link',
        'ol', 'ul', 'blockquote', 'image', 'embed',
    ]
    icon = "pilcrow"


class BaseCardBlock(StructBlock):
    heading = CharBlock(form_classname="title")
    date = DateBlock()
    image = ImageChooserBlock()
    body = TextBlock()

    class Meta:
        icon = "doc-full"
        template = 'base/blocks/base_card_block.html'
