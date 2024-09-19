import pytest
from wagtail.models import Page, Site


@pytest.fixture(scope='session')
def django_db_modify_db_settings():
    """
    Modifies the DATABASES settings to use the predefined test database.
    """
    from django.conf import settings
    settings.DATABASES['default']['NAME'] = settings.DB_TEST_NAME


@pytest.fixture
def site(db):
    """
    Fixture to create a site.
    """
    # Get or create the root page
    root = Page.get_first_root_node()
    if not root:
        root = Page(title="Root", slug="root")
        root.save_revision().publish()

    # Create a site
    site = Site.objects.create(
        hostname="testserver",
        root_page=root,
        is_default_site=True,
        site_name="testserver",
    )
    return site
