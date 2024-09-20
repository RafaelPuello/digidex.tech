import pytest


@pytest.fixture
def user_data():
    return {
        'username': 'testuser',
        'password': 'testpass123',
        'email': 'testuser@example.com',
        'first_name': 'Test',
        'last_name': 'User'
    }
