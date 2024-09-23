from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import NFCTag

User = get_user_model()


class NFCTagDesignModelTest(TestCase):
    def setUp(self):
        """
        Set up the test environment.
        """
        self.user = User.objects.create(username="testuser")

    def test_str_representation(self):
        """
        Test the string representation of the model.
        """
        self.assertEqual(str(self.ntag_design), "Test Design")
