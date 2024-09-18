import pytest
from selenium import webdriver
from django.contrib.auth import get_user_model

from home.tests.factories import (
    LocaleFactory,
    HomePageFactory
)
from trainers.tests.factories import (
    TrainerFactory,
    TrainerPageFactory
)

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
def locale(db):
    return LocaleFactory()


@pytest.fixture
def home_page(db, locale):
    return HomePageFactory(locale=locale)


@pytest.fixture
def trainer(db, home_page):
    """
    Creates a Trainer instance along with its associated Collection.
    The Collection is automatically created with the Trainer's UUID.
    """
    return TrainerFactory(home_page=home_page)


@pytest.fixture
def trainer_collection(db, trainer):
    """
    Returns the Collection associated with the given Trainer.
    """
    return trainer.collection


@pytest.fixture
def trainer_group(db, trainer):
    """
    Returns the Group associated with the given Trainer.
    """
    return trainer.group


@pytest.fixture
def trainer_page(db, trainer, home_page):
    return TrainerPageFactory(owner=trainer, locale=home_page.locale)


@pytest.fixture
def request_factory():
    from django.test import RequestFactory
    return RequestFactory()
