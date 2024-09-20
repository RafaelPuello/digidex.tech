import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()


@pytest.mark.django_db
def test_user_creation(user_data):
    user = User.objects.create_user(**user_data)
    
    assert user.uuid is not None
    assert user.created_at is not None
    assert user.last_modified is not None
    assert str(user) == f"{user_data['first_name']} {user_data['last_name']} ({user_data['username']})"


@pytest.mark.django_db
def test_user_delete_removes_associated_group(user_data):
    # Create a user
    user = User.objects.create_user(**user_data)

    # Create a group with the same name as the user's UUID
    user_group = Group.objects.create(name=user.uuid)
    assert Group.objects.filter(name=user.uuid).exists()

    # Delete the user
    user.delete()

    # The associated group should also be deleted
    assert not Group.objects.filter(name=user.uuid).exists()
