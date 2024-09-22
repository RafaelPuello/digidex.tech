from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class NFCTagDesignModelTest(TestCase):

    def setUp(self):
        # Set up initial data for tests
        self.user = User.objects.create(username="testuser")

    def test_str_representation(self):
        """Test the string representation of the model."""
        self.assertEqual(str(self.ntag_design), "Test Design")
