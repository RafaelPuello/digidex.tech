from wagtail.blocks import (
    BooleanBlock,
    CharBlock,
    ChoiceBlock,
    DateBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock
)
from wagtail.images.blocks import ImageChooserBlock


class CardImageBlock(StructBlock):
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
        template = "base/blocks/card_image_block.html"


class CardHeadingBlock(StructBlock):
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
        template = "base/blocks/card_heading_block.html"


class CardDateBlock(StructBlock):
    header = BooleanBlock(required=False)
    date = DateBlock(required=True)

    class Meta:
        icon = "date"
        template = "base/blocks/card_date_block.html"


class CardBodyBlock(RichTextBlock):
    features = [
        'bold', 'italic', 'link',
        'ol', 'ul', 'blockquote',
        'image', 'embed',
        'h4', 'h5'
    ]
    icon = "pilcrow"


class CardBlock(StreamBlock):
    heading = CardHeadingBlock(required=False)
    date = CardDateBlock()
    image = CardImageBlock(required=False)
    body = CardBodyBlock()

    class Meta:
        icon = "doc-full"
        template = 'base/blocks/card_block.html'
