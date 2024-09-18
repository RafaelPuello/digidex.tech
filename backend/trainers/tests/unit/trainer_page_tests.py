import pytest

from trainers.models import TrainerPage


@pytest.mark.django_db
def test_trainer_page_creation(user, homepage):
    trainer_page = TrainerPage(
        title=user.username,
        slug=user.username,
        owner=user
    )
    homepage.add_child(instance=trainer_page)
    trainer_page.save_revision().publish()

    # Check the user page was created and is accessible
    assert TrainerPage.objects.filter(slug=user.username).exists()
    assert trainer_page.get_trainer_inventories() == user.get_inventories()
