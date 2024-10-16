from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock
)
from wagtail.images.blocks import ImageChooserBlock


class ImageBlock(StructBlock):
    image = ImageChooserBlock(
        required=True
    )
    caption = CharBlock(
        required=False
    )
    attribution = CharBlock(
        required=False
    )

    class Meta:
        icon = "image"
        template = "base/blocks/image_block.html"


class HeadingBlock(StructBlock):
    heading_text = CharBlock(
        classname="title",
        required=True
    )
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
        template = "base/blocks/heading_block.html"


class BodyBlock(RichTextBlock):
    features = [
        'bold', 'italic', 'link',
        'ol', 'ul', 'blockquote', 
        'image', 'embed',
        'h4', 'h5'
    ]
    icon = "pilcrow"


class BaseStreamBlock(StreamBlock):
    heading = HeadingBlock()
    image = ImageBlock()
    body = BodyBlock()

    class Meta:
        template = 'base/blocks/stream_block.html'
