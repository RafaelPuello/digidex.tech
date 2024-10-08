import uuid
from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, TabbedInterface, TitleFieldPanel, ObjectList
from wagtail.contrib.routable_page.models import RoutablePageMixin, path

from base.models import CollectionMixin
from base.utils import assign_wagtail_group_permissions


COLLECTION_PERMISSIONS = (
    'add_image', 'change_image', 'choose_image',
    'add_document', 'change_document', 'choose_document'
)

PAGE_PERMISSIONS = (
    'add_page', 'publish_page'
)


class InventoryIndexCollection(CollectionMixin, models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='index_collection'
    )

    def __str__(self):
        return f"{self.user.username}'s collection"

    class Meta:
        verbose_name = _('index collection')
        verbose_name_plural = _('index collections')

    def save(self, *args, **kwargs):
        if not self.collection:
            self.collection = self.get_for_user(self.user)
        super().save(*args, **kwargs)

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
            _instance = cls.objects.get(
                user=user
            )
            return _instance
        except cls.DoesNotExist:
            user_collection = cls.get_user_collection(user)
            _instance = cls.objects.create(
                user=user,
                collection=user_collection
            )
            group = user.get_user_group()
            assign_wagtail_group_permissions(group, _instance, COLLECTION_PERMISSIONS)
            return _instance

    def get_user_page(self):
        return InventoryIndexPage.get_for_user(self.user)


class InventoryIndexPage(Page):

    user_collection = models.OneToOneField(
        'inventory.InventoryIndexCollection',
        on_delete=models.PROTECT,
        related_name='page'
    )

    parent_page_types = [
        'home.HomePage'
    ]
    child_page_types = [
        'inventory.InventoryBoxPage'
    ]

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

    def __str__(self):
        return f"{self.user_collection} and page"

    class Meta:
        verbose_name = _('user home page')
        verbose_name_plural = _('user home pages')

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
        boxes_q = InventoryBoxPage.objects.descendant_of(self).live().specific()

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
        from botany.models import UserPlant
        plants_q = UserPlant.objects.filter(box__in=self.get_boxes())

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
        from home.models import HomePage
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
        user_collection = InventoryIndexCollection.get_for_user(user)

        try:
            return cls.objects.get(user_collection=user_collection)
        except cls.DoesNotExist:
            # Create unsaved page
            _instance = cls(
                title=user.username,
                slug=slugify(user.username),
                owner=user,
                user_collection=user_collection
            )
            # Add it to the parent page
            parent_page = cls.get_parent_page()
            parent_page.add_child(instance=_instance)
            # Save, publish, and return the page
            _instance.save_revision().publish()
            group = user.get_user_group()
            assign_wagtail_group_permissions(group, _instance, PAGE_PERMISSIONS)
            return _instance

    @property
    def collection(self):
        return self.user_collection.collection


class InventoryBoxPage(RoutablePageMixin, Page):

    description = models.TextField(
        blank=True
    )
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True
    )

    parent_page_types = [
        'inventory.InventoryIndexPage'
    ]
    child_page_types = []

    content_panels = [
        TitleFieldPanel('title', classname="title"),
        FieldPanel('slug'),
        FieldPanel('description'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Details'),
        ObjectList(Page.promote_panels, heading='Promote', permission="superuser"),
        ObjectList(Page.settings_panels, heading='Settings', permission="superuser"),
    ])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('box')
        verbose_name_plural = _('boxes')

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['plants'] = self.get_plants()
        return context

    @path('<slug:plant_slug>/')
    def plant_details(self, request, plant_slug):
        from botany.models import UserPlant
        plant = get_object_or_404(UserPlant, slug=plant_slug, box=self)
        return self.render(
            request,
            context_overrides={'plant': plant},
            template="inventory/inventory_detail_page.html"
        )

    def get_plants(self):
        from botany.models import UserPlant
        return UserPlant.objects.filter(box=self)

    @property
    def collection(self):
        return self.get_parent_collection()

    def get_parent_collection(self):
        return self.owner.index_collection.collection
