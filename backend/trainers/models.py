import uuid
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AbstractUser, Group, Permission
from wagtail.models import Page, Collection
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


def get_trainer_group():
    group, created = Group.objects.get_or_create(name='Trainers')
    if created:
        group = create_trainer_group_permissions(group)
    return group


def create_trainer_group_permissions(group):
    PERMISSIONS = [
        "add_plant", "change_plant", "delete_plant",
        "add_box", "change_box", "delete_box",
        "view_nfctag", "view_nfctagtype", "view_nfctagscan", "view_nfctagmemory",
        "access_admin",
    ]

    permissions = Permission.objects.filter(
        codename__in=PERMISSIONS
    )
    group.permissions.add(*permissions)
    group.save()
    return group


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
        related_name='+'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    last_modified = models.DateTimeField(
        auto_now=True
    )

    def get_inventories(self):
        return self.inventories.all()

    def setup(self):
        """
        Sets up the trainer by creating a group and collection for them.
        """

        user_group = self.setup_group()
        collection = self.setup_collection(user_group)  # noqa: F841 - assigned for future use
        trainer_group = get_trainer_group()
        self.groups.add(trainer_group)

    def setup_group(self):
        """
        Creates a group for the trainer if it does not already exist.

        Returns:
            Group: The created or retrieved group instance.
        """

        group = Group.objects.create(name=self.uuid)
        self.groups.add(group)
        return group

    def setup_collection(self, group):
        """
        Creates a collection for the trainer if it does not already exist.
        The collection path will be: root -> trainer collection -> [user_uuid].

        Args:
            group (Group): An instance of the Group model.

        Returns:
            Collection: The created or retrieved collection instance.
        """

        # Check if the trainer already has a collection
        if self.collection:
            return self.collection

        # Get the root collection
        try:
            root_collection = Collection.get_first_root_node()
        except ObjectDoesNotExist:
            raise Exception("Root collection not found. Please ensure a root collection exists.")

        # Create the 'Trainer Collection' under the root and save it
        root_user_collection = Collection(
            name="Trainer Collections"
        )
        root_collection.add_child(instance=root_user_collection)
        root_user_collection.save()

        # Create the user's specific collection under the root 'Trainer Collections'
        user_collection = Collection(
            name=self.uuid
        )
        root_user_collection.add_child(instance=user_collection)

        # Set up the permissions for the group
        user_collection = self.setup_collection_permissions(self, group)

        # Assign the collection to the user
        self.collection = user_collection
        self.save()
        return user_collection

    def setup_collection_permissions(self, group):
        """
        Creates the necessary permissions for the given group on the given collection.
        The permissions include 'add_image', 'change_image', 'choose_image', 'add_document',
        'change_document', and 'choose_document'.

        Args:
            collection (Collection): An instance of the Collection model.
            group (Group): An instance of the Group model.
        Returns:
            Collection: The collection instance with permissions set.
        """

        PERMISSIONS = [
            "add_plant", "change_plant", "delete_plant",
            "add_box", "change_box", "delete_box",
            "view_nfctag", "view_nfctagtype", "view_nfctagscan", "view_nfctagmemory",
            "access_admin",
        ]

        permissions = Permission.objects.filter(
            codename__in=PERMISSIONS
        )
        group.permissions.add(*permissions)
        group.save()

    def create_trainer_page(self):
        from home.models import HomePage
        parent_page = HomePage.objects.first()
        trainer_page = TrainerPage(
            slug=slugify(self.username),
            title=self.username,
            owner=self
        )
        parent_page.add_child(instance=trainer_page)
        trainer_page.save_revision().publish()
        return trainer_page

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            user_group = Group.objects.get(name=self.uuid)
            user_group.delete()
            super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

    class Meta:
        verbose_name = _('trainer')
        verbose_name_plural = _('trainers')


class TrainerPage(Page):
    """
    Represents a trainer page in the database.

    Attributes:
        description (RichTextField): The description of the trainer page.
        inventory (StreamField): The inventory of the trainer page.
    """
    description = RichTextField(
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('description')
    ]

    parent_page_types = ['home.HomePage']

    child_page_types = []

    def get_context(self, request):
        context = super().get_context(request)
        context['inventories'] = self.get_trainer_inventories()
        return context

    def get_trainer_inventories(self):
        return self.owner.get_inventories()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('trainer page')
        verbose_name_plural = _('trainer pages')
