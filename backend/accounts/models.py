import uuid
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group


class User(AbstractUser):
    """
    Represents a user in the database.

    Attributes:
        uuid (uuid): A unique identifier for the user.

        username (str): The username of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email address of the user.
        groups (list): The groups the user belongs to.
        user_permissions (list): The permissions the user has.
        is_staff (bool): Whether the user is a staff member.
        is_active (bool): Whether the user is active.
        is_superuser (bool): Whether the user is a superuser.
        last_login (datetime): The date and time the user last logged in.
        date_joined (datetime): The date and time the user joined.
    """

    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        db_index=True,
    )

    def get_user_group(self):
        group, created = Group.objects.get_or_create(name=self.uuid)
        if created:
            self.groups.add(group)
        return group

    def delete_user_group(self):
        group = self.get_user_group()
        group.delete()

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            self.delete_user_group()
            super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
