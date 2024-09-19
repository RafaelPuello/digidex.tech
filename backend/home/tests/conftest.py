import pytest
from selenium.webdriver import Firefox, FirefoxOptions

from home.models import HomePage


@pytest.fixture
def homepage(db, site):
    """
    Fixture to create a homepage for Wagtail tests.
    """
    root = site.root_page
    home = HomePage(title="Home")
    root.add_child(instance=home)
    home.save_revision().publish()
    return home


@pytest.fixture(scope="class")
def browser():
    """
    Fixture to set up a browser for Selenium tests.
    """
    options = FirefoxOptions()
    options.headless = True
    driver = Firefox(options=options)
    yield driver
    driver.quit()
