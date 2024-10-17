from wagtail.blocks import BooleanBlock, CharBlock, DateBlock, RichTextBlock, StructBlock
from wagtail.images.blocks import ImageChooserBlock
from base.blocks import BaseStreamBlock


class PostBlock(StructBlock):
    title = CharBlock(
        required=True,
        help_text="Title of the post"
    )
    date = DateBlock(
        required=True,
        help_text="Publication date"
    )
    main_image = ImageChooserBlock(
        required=False,
        help_text="Main image for the post"
    )
    body = RichTextBlock(
        features=["bold", "italic", "link"],
        help_text="Content of the post"
    )
    featured = BooleanBlock(
        required=False,
        help_text="Check if this post should be featured"
    )

    class Meta:
        icon = "doc-full"
        template = "blog/blocks/post_block.html"


class BlogStreamBlock(BaseStreamBlock):
    post = PostBlock()
