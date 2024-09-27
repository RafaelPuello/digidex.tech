from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from wagtail.models import Page, Collection
from wagtail.fields import RichTextField
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    TabbedInterface,
    ObjectList
)
from wagtail.contrib.forms.models import AbstractForm, AbstractFormField
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from modelcluster.fields import ParentalKey


class UserIndexCollection(models.Model):
    """
    Represents a user's collection.

    Attributes:
        user (User): The user who owns the collection.
        collection (Collection): The collection that belongs to the user.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='collection'
    )
    collection = models.OneToOneField(
        Collection,
        on_delete=models.PROTECT,
        related_name='+'
    )

    def create_user_page(self):
        root_page = UserIndexPage.get_root_page()
        user_slug = slugify(self.user.username)
        try:
            return root_page.get_children().get(slug=user_slug)
        except Page.DoesNotExist:
            user_page = UserIndexPage(
                title=self.user.username,
                slug=user_slug,
                owner=self.user,
                user_collection=self
            )
            root_page.add_child(instance=user_page)
            user_page.save_revision().publish()
            return user_page

    @staticmethod
    def get_root_collection():
        root = Collection.get_first_root_node()
        if not root:
            raise Exception("Root collection not found. Please ensure a root collection exists.")
        return root

    @classmethod
    def get_for_user(cls, user):
        root = cls.get_root_collection()
        try:
            collection = root.get_children().get(name=str(user.uuid))
        except Collection.DoesNotExist:
            collection = root.add_child(instance=Collection(name=str(user.uuid)))
        return cls.objects.get_or_create(user=user, collection=collection)[0]

    def __str__(self):
        return f"{self.user.username}'s collection"

    class Meta:
        verbose_name = _('user collection')
        verbose_name_plural = _('user collections')


class UserIndexPage(Page):
    """
    Represents a user's index page.

    Attributes:
        user_collection (UserIndexCollection): The user collection that the page belongs to.
    """
    user_collection = models.OneToOneField(
        UserIndexCollection,
        on_delete=models.PROTECT,
        related_name='page'
    )

    shared_panels = [
    ]

    private_panels = [
        FieldPanel('user_collection')
    ]

    edit_handler = TabbedInterface([
        ObjectList(shared_panels, heading='Details'),
        ObjectList(private_panels, heading='Admin only', permission="superuser"),
        # ObjectList(Page.promote_panels, heading='Promote'),
        # ObjectList(Page.settings_panels, heading='Settings'), # The default settings are now displayed in the sidebar but need to be in the `TabbedInterface`.
    ])

    parent_page_types = [
        'home.HomePage'
    ]

    child_page_types = [
        'home.UserFormPage'
    ]

    @staticmethod
    def get_root_page():
        root = HomePage.objects.first()
        if not root:
            raise Exception("home page not found. Please ensure a home page exists.")
        return root

    def __str__(self):
        return f"{self.user_collection} and  page"

    class Meta:
        verbose_name = _('user home page')
        verbose_name_plural = _('user home pages')


class UserFormField(AbstractFormField):
    page = ParentalKey(
        'home.UserFormPage',
        on_delete=models.CASCADE,
        related_name='form_fields'
    )


class UserFormPage(AbstractForm):
    intro = RichTextField(
        blank=True
    )
    thank_you_text = RichTextField(
        blank=True
    )

    content_panels = AbstractForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('intro'),
        InlinePanel('form_fields', label="Form fields")
    ]

    parent_page_types = [
        'home.UserIndexPage'
    ]

    child_page_types = []

    def __str__(self):
        if self.owner:
            return f"{self.owner.username}'s form page."
        return f"Form page with no owner."

    class Meta:
        verbose_name = _('user form page')
        verbose_name_plural = _('user form pages')


class HomePage(Page):
    """
    Represents the homepage of the website.

    Attributes:
        intro (TextField): The introduction of the page.
        body (RichTextField): The body of the page.
    """
    intro = models.TextField(
        blank=True
    )
    body = RichTextField(
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
    ]

    parent_page_types = [
        'wagtailcore.Page'
    ]

    child_page_types = [
        'home.UserIndexPage',
        'blog.BlogIndexPage',
        'blog.TagIndexPage',
        'company.CompanyIndexPage',
        'support.ContactFormPage',
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('home page')
        verbose_name_plural = _('home pages')
