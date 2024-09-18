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


@pytest.fixture(scope="class")
def browser():
    # Set up the browser once for all tests in this class
    options = webdriver.FirefoxOptions()
    options.headless = True  # Run in headless mode for faster tests and no UI
    driver = webdriver.Firefox(options=options)
    yield driver
    # Quit the browser after all tests have run
    driver.quit()


@pytest.fixture
def homepage(db):
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
def request_factory():
    from django.test import RequestFactory
    return RequestFactory()
