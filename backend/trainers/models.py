import uuid
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser, Group
from wagtail.models import Page, Collection
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
