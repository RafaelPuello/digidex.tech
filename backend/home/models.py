from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _
from wagtail.models import Page, Collection
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class HomePage(Page):
    """
    Represents the homepage of the website.
    """
    body = RichTextField(
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('body')
    ]

    parent_page_types = ['wagtailcore.Page']

    child_page_types = ['home.UserHomePage']

    def __str__(self):
        """
        Represents the string representation of the homepage by its title.
        """
        return self.title

    class Meta:
        verbose_name = _('homepage')


class UserHomePage(Page):
    """
    Represents the homepage of a user.
    """
    body = RichTextField(
        blank=True
    )
    collection = models.ForeignKey(
        Collection,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='collection',
    )

    content_panels = Page.content_panels + [
        FieldPanel('body')
    ]

    parent_page_types = ['home.HomePage']

    child_page_types = []

    def setup_collection(self):
        """
        Creates a collection for the trainer if it does not already exist.
        The collection path will be: root -> trainer collection -> [user_uuid].

        Args:
            group (Group): An instance of the Group model.

        Returns:
            Collection: The created or retrieved collection instance.
        """
        group = None

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
            "view_nfctagtype",
            "view_nfctag", "change_nfctag",
            "view_nfctagscan",
            "view_nfctagmemory",
            "access_admin",
        ]

        permissions = Permission.objects.filter(
            codename__in=PERMISSIONS
        )
        group.permissions.add(*permissions)
        group.save()

    def __str__(self):
        """
        Represents the string representation of the user homepage by its title.
        """
        return self.title

    class Meta:
        verbose_name = _('user homepage')
