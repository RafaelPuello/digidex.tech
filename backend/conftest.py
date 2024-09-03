import pytest
from wagtail.models import Page
from selenium import webdriver

from inventory.models import InventoryIndex
from accounts.models import DigiDexUser


@pytest.fixture(scope="class")
def browser():
    # Set up the browser once for all tests in this class
    driver = webdriver.Firefox()
    yield driver
    # Quit the browser after all tests have run
    driver.quit()


@pytest.fixture
def home_page():
    root_page = Page.objects.get(id=1)
    home_page = InventoryIndex(title="Test Inventory", slug="test-inventory")
    root_page.add_child(instance=home_page)
    return home_page


@pytest.fixture
def new_user(db):
    return DigiDexUser.objects.create_user(username='testuser', password='testpass123')
