from wagtail import hooks
from wagtail.admin.viewsets.pages import PageListingViewSet
from wagtail.admin.panels import TabbedInterface, FieldPanel, ObjectList
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.snippets.models import register_snippet

from .models import InventoryBox, Plant


@hooks.register("register_icons")
def register_icons(icons):
    return icons + ['botany/icons/plant.svg']


class InventoryBoxViewSet(PageListingViewSet):
    """
    A view set for the InventoryBox model.
    """
    model = InventoryBox
    icon = "desktop"
    add_to_admin_menu = True
    menu_label = "Inventory"
    menu_name = "inventory"


inventory_box_listing_viewset = InventoryBoxViewSet("inventory_boxes")
@hooks.register("register_admin_viewset")
def register_inventory_box_listing_viewset():
    return inventory_box_listing_viewset


class PlantSnippetViewSet(SnippetViewSet):
    """
    A snippet view set for the Plant model.
    """
    model = Plant
    icon = "plant"
    menu_label = "Plants"
    menu_name = "plants"
    add_to_admin_menu = True

    public_panels = [
        FieldPanel("name"),
        FieldPanel("description"),
        FieldPanel("collection"),
    ]

    private_panels = [
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(public_panels, heading='Details'),
            ObjectList(private_panels, heading='Admin only', permission="superuser"),
        ]
    )

register_snippet(PlantSnippetViewSet)
