import pytest

from home.models import HomePage


@pytest.mark.django_db
def test_homepage_fixture(homepage):
    """
    Test that the homepage fixture creates a HomePage instance.
    """
    # Check if the homepage instance exists
    assert HomePage.objects.count() == 1

    # Check the title of the homepage instance
    assert homepage.title == "Home"

    # Check that the homepage has no body content initially
    assert homepage.body == ""
