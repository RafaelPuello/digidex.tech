from wagtail.blocks import BooleanBlock

from base.blocks import CardBlock


class BlogPostCardBlock(CardBlock):
    featured = BooleanBlock()
