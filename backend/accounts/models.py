import uuid
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group, Permission


def create_user_group_permissions(group):
    """
    Creates the necessary permissions for the given group.
    The permissions include 'add_image', 'change_image', 'choose_image', 'add_document',
    'change_document', and 'choose_document'.
    """
    permissions = Permission.objects.filter(
        codename__in=[
            "add_plant", "change_plant", "delete_plant",
            "add_box", "change_box", "delete_box",
            "view_nfctag", "view_nfctagdesign", "view_nfctagscan", "view_nfctagmemory",
            "access_admin",
        ]
    )
    group.permissions.add(*permissions)
    group.save()
    return group


class User(AbstractUser):
    """
    Represents a user in the database.

    Attributes:
        uuid (uuid): A unique identifier for the user.
        created_at (datetime): The date and time the user was created.
        last_modified (datetime): The date and time the user was last updated.
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

    def get_inventory(self):
        """
        Returns all inventory boxes of the user.
        """
        return self.boxes.all()

    def delete(self, *args, **kwargs):
        """
        Deletes the user and the associated group.
        """
        with transaction.atomic():
            user_group = Group.objects.get(name=self.uuid)
            user_group.delete()
            super().delete(*args, **kwargs)

    def __str__(self):
        """
        A string representation of the user.
        """
        return f"{self.first_name} {self.last_name} ({self.username})"

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
