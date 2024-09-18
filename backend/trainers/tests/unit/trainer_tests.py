import pytest
from wagtail.models import Collection

from trainers.models import Trainer


@pytest.mark.django_db
def test_trainer_creation(user):
    assert isinstance(user, Trainer)
    assert user.groups.filter(name='Trainers').exists()
    assert user.collection is not None


@pytest.mark.django_db
def test_trainer_collection_setup(user):
    root_collection = Collection.get_first_root_node()
    assert root_collection is not None
    assert user.collection.get_ancestors().filter(id=root_collection.id).exists()


@pytest.mark.django_db
def test_trainer_group_permissions(user):
    group = user.groups.get(name=user.uuid)
    expected_permissions = ["add_plant", "change_plant", "delete_plant", "access_admin"]
    group_permissions = list(group.permissions.values_list("codename", flat=True))
    
    for perm in expected_permissions:
        assert perm in group_permissions
