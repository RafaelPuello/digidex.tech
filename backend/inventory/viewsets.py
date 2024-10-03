from wagtail.admin.viewsets.pages import PageListingViewSet
from wagtail.admin.viewsets.chooser import ChooserViewSet

from .models import InventoryBoxPage


class BoxListingViewSet(PageListingViewSet):
    model = InventoryBoxPage
    icon = "desktop"
    menu_order = 110
    menu_label = "Inventory"
    menu_name = "inventory"
    copy_view_enabled = False
    inspect_view_enabled = True
    admin_url_namespace = "boxes"
    base_url_path = "inventory/boxes"
    add_to_admin_menu = True


class BoxChooserViewSet(ChooserViewSet):
    model = InventoryBoxPage
    icon = "desktop"
    choose_one_text = "Choose a box"
    edit_item_text = "Edit this box"
    form_fields = ["title", "slug", "description"]

    def get_object_list(self):
        return InventoryBoxPage.objects.filter(owner=self.request.user)


box_listing_viewset = BoxListingViewSet('boxes')
box_chooser_viewset = BoxChooserViewSet("box_chooser")
