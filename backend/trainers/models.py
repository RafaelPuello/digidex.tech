import uuid
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser, Group, Permission
from wagtail.models import Page, Collection, GroupPagePermission, GroupCollectionPermission
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel

from inventory.blocks import InventoryBlock
from .utils import create_trainer_collection


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
    collection = models.ForeignKey(
        Collection,
        null=True,
        on_delete=models.SET_NULL,
        related_name='trainers'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    last_modified = models.DateTimeField(
        auto_now=True
    )

    def get_inventories(self):
        return self.inventories.all()

    def set_trainer_group(self):
        trainer_group, created = Group.objects.get_or_create(name=f"trainer_{self.uuid}")
        if created:
            self.groups.add(trainer_group)
        return trainer_group

    def set_image_permissions(self, collection, group):
        IMAGE_PERMISSIONS = (
            'add_image', 'change_image', 'choose_image'
        )

        for perm in IMAGE_PERMISSIONS:
            permission = Permission.objects.get(codename=perm)
            GroupCollectionPermission.objects.create(
                group=group,
                collection=collection,
                permission=permission
            )
        return

    def set_document_permissions(self, collection, group):
        DOCUMENT_PERMISSIONS = (
            'add_document', 'change_document', 'choose_document'
        )

        for perm in DOCUMENT_PERMISSIONS:
            permission = Permission.objects.get(codename=perm)
            GroupCollectionPermission.objects.create(
                group=group,
                collection=collection,
                permission=permission
            )
        return

    def set_collection(self, group):
        if not self.collection:
            create_trainer_collection(self)
        self.set_image_permissions(self.collection, group)
        self.set_document_permissions(self.collection, group)
        return

    def set_page_permissions(self, page, group):
        PAGE_PERMISSIONS = ('change_page', 'publish_page')

        for perm in PAGE_PERMISSIONS:
            permission = Permission.objects.get(codename=perm)
            GroupPagePermission.objects.create(
                group=group,
                page=page,
                permission=permission
            )
        return

    def set_page(self, group):
        if not hasattr(self, 'page'):
            TrainerPage.create_for_trainer(self)
        self.set_page_permissions(self.page, group)
        return

    @transaction.atomic
    def user_setup(self):
        PERMISSIONS = [
            # Wagtail snippet permissions
            "view_nfctagscan", "view_nfctagtype",
            # Wagtail admin dashboard permissions
            'access_admin',
        ]

        trainer_group = self.set_trainer_group()
        self.set_collection(trainer_group)
        self.set_page(trainer_group)

        permissions = Permission.objects.filter(
            codename__in=PERMISSIONS
        )
        trainer_group.permissions.add(*permissions)
        trainer_group.save()
        return

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            user_group = Group.objects.get(name=f"trainer_{self.uuid}")
            user_group.delete()
            super().delete(*args, **kwargs)

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
    trainer = models.OneToOneField(
        Trainer,
        null=True,
        on_delete=models.SET_NULL,
        related_name='page'
    )
    description = RichTextField(
        blank=True
    )
    body = StreamField([
        ('inventory', InventoryBlock())
    ])

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('body')
    ]

    parent_page_types = ['home.HomePage']

    child_page_types = []

    @classmethod
    def create_for_trainer(cls, trainer):
        from home.models import HomePage
        parent_page = HomePage.objects.first()
        trainer_page = cls(
            slug=slugify(trainer.username),
            title=trainer.username,
            owner=trainer,
            trainer=trainer
        )
        parent_page.add_child(instance=trainer_page)
        trainer_page.save_revision().publish()
        return trainer_page

    def get_context(self, request):
        context = super().get_context(request)
        context['inventories'] = self.get_trainer_inventories()
        return context

    def get_trainer_inventories(self):
        return self.trainer.get_inventories()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('trainer page')
        verbose_name_plural = _('trainer pages')
