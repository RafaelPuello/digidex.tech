from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index

from base.models import GalleryImageMixin


class BlogIndexPage(Page):
    intro = RichTextField(
        blank=True
    )

    parent_page_types = [
        'home.HomePage'
    ]
    child_page_types = [
        'blog.BlogPage'
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)

        posts = self.get_children().live().order_by('-first_published_at').specific()
        context['posts'] = posts

        featured = posts.filter(blogpage__featured=True)
        context['featured_posts'] = featured
        return context


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class TagIndexPage(Page):
    parent_page_types = [
        'home.HomePage'
    ]
    child_page_types = []

    def get_context(self, request):
        """
        Filter blog pages by tag and update template context
        """
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)

        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context


class BlogPage(Page):
    date = models.DateField(
        "Post date"
    )
    intro = models.CharField(
        max_length=250
    )
    body = RichTextField(
        blank=True
    )
    featured = models.BooleanField(
        default=False
    )

    tags = ClusterTaggableManager(
        through=BlogPageTag,
        blank=True
    )

    parent_page_types = [
        'blog.BlogIndexPage'
    ]
    child_page_types = []

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),

    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('featured'),
                FieldPanel('date'),
                FieldPanel('tags'),
            ], heading="Blog information"),
        FieldPanel('intro'),
        FieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]


class BlogPageGalleryImage(GalleryImageMixin):
    page = ParentalKey(
        BlogPage,
        on_delete=models.CASCADE,
        related_name='gallery_images'
    )
