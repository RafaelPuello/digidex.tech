from django.db import models
from django.conf import settings
from django.contrib.auth.models import Permission
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from wagtail.models import Page, GroupCollectionPermission
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, TabbedInterface, ObjectList

from base.models import CollectionMixin


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

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('home page')
        verbose_name_plural = _('home pages')


class UserIndexPage(Page):
    """
    Represents a user's index page.

    Attributes:
        user_collection (UserIndexCollection): The user collection that the page belongs to.
    """
    user_collection = models.OneToOneField(
        'home.UserIndexCollection',
        on_delete=models.PROTECT,
        related_name='page'
    )

    parent_page_types = [
        'home.HomePage'
    ]
    child_page_types = []

    shared_panels = []
    private_panels = [
        FieldPanel('user_collection')
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(shared_panels, heading='Details'),
            ObjectList(private_panels, heading='Admin only', permission="superuser"),
        ]
    )

    @staticmethod
    def get_root_page():
        root = HomePage.objects.first()
        if not root:
            raise Exception("home page not found. Please ensure a home page exists.")
        return root

    def set_permissions(self):
        PAGE_PERMISSIONS = (
            'add_page', 'publish_page'
        )

        group = self.owner.get_user_group()
        for perm in PAGE_PERMISSIONS:
            permission = Permission.objects.get(codename=perm)
            GroupCollectionPermission.objects.create(
                group=group,
                collection=self,
                permission=permission
            )
        return

    def __str__(self):
        return f"{self.user_collection} and page"

    class Meta:
        verbose_name = _('user home page')
        verbose_name_plural = _('user home pages')


class UserIndexCollection(CollectionMixin, models.Model):
    """
    Represents a user's collection.

    Attributes:
        user (User): The user who owns the collection.
        collection (Collection): The collection that belongs to the user.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='index_collection'
    )

    def create_user_page(self):
        root_page = UserIndexPage.get_root_page()
        user_slug = slugify(self.user.username)
        try:
            return root_page.get_children().get(slug=user_slug).specific
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

    @classmethod
    def get_parent_collection(cls):
        root = cls.get_root_collection()
        if not root:
            raise Exception("Root collection not found. Please ensure a root collection exists.")
        return cls.get_or_create_collection(name='Users', parent=root)

    @classmethod
    def get_collection_for_user(cls, user):
        parent_collection = cls.get_parent_collection()
        return cls.get_or_create_collection(name=str(user.uuid), parent=parent_collection)

    @classmethod
    def get_for_user(cls, user):
        collection = cls.get_collection_for_user(user)
        instance, created = cls.objects.update_or_create(
            user=user,
            defaults={'collection': collection}
        )
        return instance

    def set_permissions(self):
        COLLECTION_PERMISSIONS = (
            'add_image', 'change_image', 'choose_image',
            'add_document', 'change_document', 'choose_document'
        )

        group = self.user.get_user_group()
        for perm in COLLECTION_PERMISSIONS:
            permission = Permission.objects.get(codename=perm)
            GroupCollectionPermission.objects.create(
                group=group,
                collection=self.collection,
                permission=permission
            )
        return

    def save(self, *args, **kwargs):
        if not self.collection:
            self.collection = self.get_collection_for_user(self.user)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s collection"

    class Meta:
        verbose_name = _('user collection')
        verbose_name_plural = _('user collections')
