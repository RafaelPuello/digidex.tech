from wagtail import hooks

from .viewsets import box_listing_viewset, box_chooser_viewset


@hooks.register("register_admin_viewset")
def register_viewset():
    return [box_listing_viewset, box_chooser_viewset]
