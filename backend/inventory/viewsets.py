from wagtail.admin.views.generic.chooser import ChooseView
from wagtail.admin.viewsets.chooser import ChooserViewSet
from wagtail.admin.viewsets.pages import PageListingViewSet

from .models import InventoryBox


class BoxListingViewSet(PageListingViewSet):
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


class BoxChooserView(ChooseView):
    def get_object_list(self):
        # import requests
        # from django.conf import settings
        # r = requests.get(f"{settings.WAGTAILADMIN_BASE_URLquit}/api/users/")
        # r.raise_for_status()
        # results = r.json()
        # return results
        return InventoryBox.objects.filter(owner=self.request.user)


class BoxChooserViewSet(ChooserViewSet):
    model = InventoryBox
    icon = "desktop"
    choose_one_text = "Choose a box"
    edit_item_text = "Edit this box"
    form_fields = ["title", "slug", "description"]
    choose_view_class = BoxChooserView


box_listing_viewset = BoxListingViewSet('boxes')
box_chooser_viewset = BoxChooserViewSet("box_chooser")
