from wagtail import hooks
from wagtail.admin.viewsets.model import ModelViewSet, ModelViewSetGroup
from wagtail.admin.viewsets.pages import PageListingViewSet
from wagtail.admin.panels import TabbedInterface, FieldPanel, ObjectList

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
    menu_label = "Inventory"
    menu_name = "inventory"
    copy_view_enabled = False
    inspect_view_enabled = True
    admin_url_namespace = "boxes"
    base_url_path = "inventory/boxes"


class PlantModelViewSet(ModelViewSet):
    """
    A model view set for Plants.
    """
    model = Plant
    icon = "plant"
    menu_label = "Plants"
    menu_name = "plants"
    copy_view_enabled = False
    inspect_view_enabled = True
    admin_url_namespace = "plants"
    base_url_path = "inventory/plants"

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


class InventoryModelViewSetGroup(ModelViewSetGroup):
    menu_label = "Inventory"
    menu_icon = "desktop"
    menu_order = 125
    add_to_admin_menu = True
    items = (BoxModelViewSet("boxes"), PlantModelViewSet)


@hooks.register("register_admin_viewset")
def register_viewset():
    return InventoryModelViewSetGroup()
