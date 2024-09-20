import uuid
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group


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

    def delete(self, *args, **kwargs):
        """
        Deletes the user and the associated group.
        """
        with transaction.atomic():
            user_group = Group.objects.get(name=self.uuid)
            user_group.delete()
            super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
