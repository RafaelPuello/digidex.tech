from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from home.models import HomePage


class HomePageTests(WagtailPageTestCase):
    """
    Test class for HomePage model.
    """
    @classmethod
    def setUpTestData(cls):
        root = Page.get_first_root_node()
        Site.objects.create(
            hostname="testserver",
            root_page=root,
            is_default_site=True,
            site_name="testserver",
        )
        home = HomePage(title="Home Test", slug="home-test")
        root.add_child(instance=home)
        cls.page = home
