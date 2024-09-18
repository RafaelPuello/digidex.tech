import pytest
from selenium import webdriver
from django.contrib.auth import get_user_model
from wagtail.models import Page, Site

from home.models import HomePage

User = get_user_model()


@pytest.fixture(scope='session')
def django_db_setup():
    from django.conf import settings
    settings.DATABASES['default']['NAME'] = settings.DB_TEST_NAME


@pytest.fixture
def homepage(db):
    """
    Fixture to create a homepage for Wagtail tests.
    """

    home = HomePage(title="Home")

    root = Page.get_first_root_node()
    root.add_child(instance=home)

    home.save_revision().publish()
    Site.objects.create(
        hostname="testserver",
        root_page=home,
        is_default_site=True,
        site_name="testserver",
    )
    return home


@pytest.fixture
def user(db):
    """
    Fixture to create a User for testing.
    """

    return User.objects.create_user(
        username="testuser",
        password="testpassword",
        first_name="Test",
        last_name="User",
    )


@pytest.fixture(scope="class")
def browser():
    """
    Fixture to set up a browser for Selenium tests.
    """

    options = webdriver.FirefoxOptions()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    yield driver
    driver.quit()
