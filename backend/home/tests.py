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

    def test_get(self):
        response = self.client.get(self.page.url)
        self.assertEqual(response.status_code, 200)

    def test_can_create_page(self):
        self.assertCanCreateAt(Page, HomePage)

    def test_editability(self):
        self.assertPageIsEditable(self.page)

    def test_editability_on_post(self):
        self.assertPageIsEditable(
            self.page,
            post_data={
                "title": "Udpated Home Page",
                "slug": "home-test",
                "show_featured": True,
                "show_expired": False,
                "action-publish": "",
            }
        )

    def test_general_previewability(self):
        self.assertPageIsPreviewable(self.page)

    def test_archive_previewability(self):
        pass
