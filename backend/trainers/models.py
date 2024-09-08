import uuid
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group, Permission
from wagtail.models import Page, GroupPagePermission, GroupCollectionPermission
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class Trainer(AbstractUser):
    """
    Represents a trainer in the database.

    Attributes:
        uuid (uuid): A unique identifier for the trainer.
        created_at (datetime): The date and time the trainer was created.
        last_modified (datetime): The date and time the trainer was last updated.
    """

    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        db_index=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    last_modified = models.DateTimeField(
        auto_now=True
    )

    def get_user_pages(self):
        """
        Retrieve pages owned by the user.

        Returns:
            QuerySet: Filtered and ordered queryset of pages owned by the user.
        """
        return Page.objects.filter(owner=self).order_by('depth')

    def get_inventory_page(self):
        """
        Retrieve user inventory page.

        Returns:
            Page: User inventory page.
        """
        return self.get_user_pages().first().specific

    def get_inventory(self):
        """
        Retrieve user inventory.

        Returns:
            QuerySet: Filtered and ordered queryset of pages owned by the user.
        """
        usr_inv_page = self.get_inventory_page()
        if usr_inv_page:
            return usr_inv_page.get_inventory()

    @transaction.atomic
    def set_user_permissions(self, user_page):
        PAGE_PERMISSIONS = ('add_page', 'change_page', 'delete_page', 'publish_page')
        IMAGE_PERMISSIONS = ('add_image', 'change_image', 'choose_image')
        DOCUMENT_PERMISSIONS = ('add_document', 'change_document', 'choose_document')
        BASE_PERMISSIONS = [
            'add_document', 'change_document', 'choose_document',
            'add_image', 'change_image', 'choose_image',
            'access_admin',
        ]
        SNIPPET_PERMISSIONS = [
            "view_nfctagscan", "view_nfctagtype"
        ]
        user_group, created = Group.objects.get_or_create(name=f"user_{self.username}")
        if hasattr(user_page, 'collection'):
            user_collection = user_page.collection
        else:
            user_collection = user_page.create_collection()

        if created:
            for page_perm in PAGE_PERMISSIONS:
                page_permission = Permission.objects.get(codename=page_perm)
                GroupPagePermission.objects.create(
                    group=user_group,
                    page=user_page,
                    permission=page_permission
                )
            for image_perm in IMAGE_PERMISSIONS:
                image_permission = Permission.objects.get(codename=image_perm)
                GroupCollectionPermission.objects.create(
                    group=user_group,
                    collection=user_collection,
                    permission=image_permission
                )

            for document_perm in DOCUMENT_PERMISSIONS:
                document_permission = Permission.objects.get(codename=document_perm)
                GroupCollectionPermission.objects.create(
                    group=user_group,
                    collection=user_collection,
                    permission=document_permission
                )

            # Fetch all necessary permissions once
            permissions = Permission.objects.filter(
                codename__in=BASE_PERMISSIONS + SNIPPET_PERMISSIONS
            )
            user_group.permissions.add(*permissions)
            user_group.save()

            # Step 3: Assign the user to the group
            self.groups.add(user_group)
            self.save()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class TrainerPage(Page):
    """
    Represents a trainer page in the database.

    Attributes:
        body (RichTextField): The body of the trainer page.
    """
    body = RichTextField(
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('body')
    ]

    parent_page_types = ['home.HomePage']

    child_page_types = []

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('trainer page')
        verbose_name_plural = _('trainer pages')
