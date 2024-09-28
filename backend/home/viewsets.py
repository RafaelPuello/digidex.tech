from wagtail.admin.viewsets.chooser import ChooserViewSet
from wagtail.models import Page

class PageContentChooserViewSet(ChooserViewSet):
    model = Page
    url_filter_parameters = ["nfc_tag_type"]
    preserve_url_parameters = ["multiple", "nfc_tag_type"]
