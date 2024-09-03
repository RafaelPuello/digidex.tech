from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.contrib.routable_page.models import RoutablePageMixin

from .base import AbstractInventory


class InventoryIndex(RoutablePageMixin, AbstractInventory):

    content_panels = AbstractInventory.content_panels + [FieldPanel('collection')]

    parent_page_types = ['wagtailcore.Page']

    child_page_types = ['inventory.InventoryUserPage']

    template = 'inventory/inventory_index.html'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('inventory index')


class UserInventory(AbstractInventory):

    parent_page_types = ['inventory.InventoryIndex']

    subpage_types = ['inventory.Entity']

    template = 'inventory/user_inventory.html'

    def get_context(self, request):
        context = super().get_context(request)
        from ..serializers import InventoryEntitySerializer
        entities = self.get_entities()
        entities = InventoryEntitySerializer(entities, many=True).data
        context.update({'entities': entities})
        return context

    def get_entities(self):
        return self.get_children().live().specific()

    def generate_prompt(self):
        entities = self.get_entities()
        prompt = f"The user's username is {self.owner.username}:\n"
        if entities:
            prompt += f"In their inventory they have {len(entities)} plants and/or pets.\n"        
        if not self.description:
            return prompt
        return f"{prompt}. The user's inventory description is: {self.description}"

    @classmethod
    def create_for_user(cls, user, parent=None):
        if not parent:
            parent = InventoryIndex.objects.first()
        user_inventory_page = cls(
            title=user.username.title(),
            owner=user,
            slug=slugify(user.username),
        )

        parent.add_child(instance=user_inventory_page)
        user_inventory_page.save_revision().publish()
        return user_inventory_page

    class Meta:
        verbose_name = _("user inventory")
        verbose_name_plural = _("user inventories")
