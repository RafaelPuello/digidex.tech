from django.db import models
from django.conf import settings
from django.contrib.auth.models import Permission
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from wagtail.models import Page, GroupCollectionPermission, GroupPagePermission
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
        'botany.UserBoxPage',
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

    def get_context(self, request):
        context = super().get_context(request)
        context['boxes'] = self.get_boxes(10)
        context['plants'] = self.get_plants(30)
        return context

    def get_boxes(self, num=None):
        """
        Get and manipulate the box queryset for the user index page.

        Args:
            num (int): The number of boxes to return. If None, return all boxes.

        Returns:
            QuerySet: The plant queryset.
        """
        from botany.models import UserBoxPage
        boxes_q = UserBoxPage.objects.descendant_of(self).live().specific()

        if not boxes_q.exists():
            return boxes_q.none()

        if num is not None:
            if isinstance(num, int) and num > 0:
                return boxes_q[:num]
            else:
                raise ValueError("The 'num' parameter must be a positive, non-zero integer.")

        return boxes_q

    def get_plants(self, num=None):
        """
        Get and manipulate the plant queryset for the user index page.

        Args:
            num (int): The number of plants to return. If None, return all plants.

        Returns:
            QuerySet: The plant queryset.
        """
        from botany.models import Plant
        plants_q = Plant.objects.filter(box__in=self.get_boxes())

        if not plants_q.exists():
            return plants_q.none()

        if num is not None:
            if isinstance(num, int) and num > 0:
                return plants_q[:num]
            else:
                raise ValueError("The 'num' parameter must be a positive, non-zero integer.")

        return plants_q[:30]

    @staticmethod
    def get_root_page():
        """
        Gets the root page for the site used in wagtail project.
        """
        root = HomePage.objects.first()
        if not root:
            raise Exception("home page not found. Please ensure a home page exists.")
        return root

    @classmethod
    def get_parent_page(cls):
        """
        Gets the parent page 'Inventory' to group all user pages.
        Each user page will be a child of this page.
        """
        return cls.get_root_page()  # TODO: Update to actual parent page

    @classmethod
    def get_for_user(cls, user):
        """
        Gets the user collection and names it after the slug
        assigned by slugifying the given user's username.
        """
        user_collection = UserIndexCollection.get_for_user(user)

        try:
            return cls.objects.get(user_collection=user_collection)
        except cls.DoesNotExist:
            # Create unsaved page
            user_page = cls(
                title=user.username,
                slug=slugify(user.username),
                owner=user,
                user_collection=user_collection
            )
            # Add it to the parent page
            parent_page = cls.get_parent_page()
            parent_page.add_child(instance=user_page)
            # Save, publish, and return the page
            user_page.save_revision().publish()
            return user_page

    def set_permissions(self):
        PAGE_PERMISSIONS = (
            'add_page', 'publish_page'
        )

        group = self.owner.get_user_group()
        for perm in PAGE_PERMISSIONS:
            permission = Permission.objects.get(codename=perm)
            GroupPagePermission.objects.create(
                group=group,
                page=self,
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

    @classmethod
    def get_parent_collection(cls):
        """
        Gets the parent collection 'Users' to group all user collections.
        Each user collection will be a child of this collection.
        """
        root = cls.get_root_collection()
        if not root:
            raise Exception("Root collection not found. Please ensure a root collection exists.")
        return cls.get_or_create_collection(name='Users', parent=root)

    @classmethod
    def get_user_collection(cls, user):
        """
        Gets the user collection and names it after the uuid assigned to the user
        for the given user.
        """
        parent_collection = cls.get_parent_collection()
        return cls.get_or_create_collection(name=str(user.uuid), parent=parent_collection)

    @classmethod
    def get_for_user(cls, user):
        """
        Gets mapping between each user and their collection. It's easier to work
        with collections like this instead of inheriting from the
        collection model and adding a user field.
        """
        try:
            instance = cls.objects.get(
                user=user
            )
        except cls.DoesNotExist:
            user_collection = cls.get_user_collection(user)
            instance = cls.objects.create(
                user=user,
                collection=user_collection
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
