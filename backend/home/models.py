from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from wagtail.models import Page, Collection
from wagtail.fields import RichTextField


class UserCollection(models.Model):
    """
    Represents a user's collection.
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
        root_page = UserPage.get_root_page()
        try:
            return root_page.get_children().get(user_collection=self)
        except Page.DoesNotExist:
            user_page = UserPage(
                title=self.user.username,
                slug=slugify(self.user.username),
                owner=self.user,
                user_collection=self
            )
            root_page.add_child(instance=user_page)
            return user_page.save_revision().publish()

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


class UserPage(Page):
    """
    Represents a user's page.
    """
    user_collection = models.OneToOneField(
        UserCollection,
        on_delete=models.PROTECT,
        related_name='page'
    )

    parent_page_types = ['home.HomePage']
    child_page_types = []

    @staticmethod
    def get_root_page():
        root = HomePage.objects.first()
        if not root:
            raise Exception("home page not found. Please ensure a home page exists.")
        return root

    def __str__(self):
        return f"{self.user_collection} and  page"

    class Meta:
        verbose_name = _('user page')
        verbose_name_plural = _('user pages')


class HomePage(Page):
    """
    Represents the homepage of the website.
    """
    body = RichTextField(
        blank=True
    )

    parent_page_types = ['wagtailcore.Page']
    child_page_types = ['home.UserPage']

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('home page')
        verbose_name_plural = _('home pages')
