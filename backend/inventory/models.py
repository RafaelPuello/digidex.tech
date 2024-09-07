from uuid import uuid4
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from wagtail.search import index
from wagtail.models import Page, Collection
from wagtail.admin.panels import FieldPanel


class UserInventory(Page):
    uuid = models.UUIDField(
        default=uuid4,
        editable=False,
        unique=True,
        db_index=True
    )
    collection = models.ForeignKey(
        Collection,
        on_delete=models.SET_NULL,
        null=True,
        related_name='+',
    )
    description = models.CharField(
        blank=True,
        max_length=250
    )

    parent_page_types = [
        'home.HomePage'
    ]

    subpage_types = []

    search_fields = Page.search_fields + [
        index.SearchField('description')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('description'),
    ]

    template = 'inventory/user_inventory.html'

    def generate_prompt(self):
        prompt = f"The user's username is {self.owner.username}:\n"
        if not self.description:
            return prompt
        return f"{prompt}. The user's inventory description is: {self.description}"

    @classmethod
    def create_for_user(cls, user, parent=None):
        if not parent:
            from home.models import HomePage
            parent = HomePage.objects.first()
        user_inventory_page = cls(
            title=user.username.title(),
            owner=user,
            slug=slugify(user.username),
        )

        parent.add_child(instance=user_inventory_page)
        user_inventory_page.save_revision().publish()
        return user_inventory_page

    def create_collection(self, title=None):
        parent_collection = Collection.get_first_root_node().get_chidren().first()
        if not parent_collection:
            return None
        if not title:
            title = self.title
        try:
            return parent_collection.get_children().get(name=title)
        except Collection.DoesNotExist:
            return parent_collection.add_child(name=title)

    def save(self, *args, **kwargs):
        if not self.collection:
            self.collection = self.create_collection()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("user inventory")
        verbose_name_plural = _("user inventories")
        indexes = [
            models.Index(fields=['uuid']),
        ]
