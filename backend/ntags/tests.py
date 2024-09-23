from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class NFCTagModelTest(TestCase):
    def setUp(self):
        """
        Set up the test environment.
        """
        self.user = User.objects.create(username="testuser")
