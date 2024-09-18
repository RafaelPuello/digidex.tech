import pytest
from unittest.mock import patch, MagicMock
from wagtail.models import Collection

from trainers.utils.collection_setup import create_user_collection


@pytest.mark.django_db
def test_create_user_collection_existing(trainer):
    """Test that create_user_collection returns existing collection if present."""
    existing_collection = trainer.collection
    returned_collection = create_user_collection(trainer)
    assert returned_collection == existing_collection


@pytest.mark.django_db
@patch('wagtail.models.Collection.get_first_root_node')
def test_create_user_collection_new(mock_get_root, trainer):
    """Test that create_user_collection creates a new collection when none exists."""
    # Mock the root collection
    mock_root = MagicMock(spec=Collection)
    mock_get_root.return_value = mock_root

    # Ensure the trainer has no collection
    trainer.collection = None
    trainer.save()

    # Call the function
    new_collection = create_user_collection(trainer)

    # Assertions
    assert new_collection.name == str(trainer.uuid)
    mock_root.add_child.assert_called_once_with(instance=new_collection)
    trainer.refresh_from_db()
    assert trainer.collection == new_collection
