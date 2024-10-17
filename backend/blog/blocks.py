from wagtail.blocks import BooleanBlock

from base.blocks import BaseCardBlock


class BlogPostCardBlock(BaseCardBlock):
    featured = BooleanBlock()
