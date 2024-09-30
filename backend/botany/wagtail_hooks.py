from wagtail import hooks
from wagtail.admin.viewsets.pages import PageListingViewSet
from wagtail.admin.panels import TabbedInterface, FieldPanel, ObjectList
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import InventoryBox, Plant


@hooks.register("register_icons")
def register_icons(icons):
    return icons + ['botany/icons/plant.svg']


class BoxModelViewSet(PageListingViewSet):
    """
    A model view set for Boxes.
    """
    model = InventoryBox
    icon = "desktop"
    menu_order = 110
    menu_label = "Inventory"
    menu_name = "inventory"
    copy_view_enabled = False
    inspect_view_enabled = True
    admin_url_namespace = "boxes"
    base_url_path = "inventory/boxes"
    add_to_admin_menu = True


@hooks.register("register_admin_viewset")
def register_inventory_box_listing_viewset():
    return BoxModelViewSet('inventory')


class PlantSnippetViewSet(SnippetViewSet):
    """
    A snippet view set for Plants.
    """
    model = Plant
    icon = "plant"
    menu_label = "Plants"
    menu_name = "plants"
    menu_order = 120
    copy_view_enabled = False
    admin_url_namespace = "inventory_plants"
    list_display = ["name", "description"]
    list_per_page = 50
    admin_url_namespace = "plants"
    base_url_path = "inventory/plants"
    add_to_admin_menu = True

    public_panels = [
        FieldPanel("box"),
        FieldPanel("name"),
        FieldPanel("description"),
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
