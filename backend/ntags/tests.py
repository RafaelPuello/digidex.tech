from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import NFCTag

User = get_user_model()


class NFCTagModelTest(TestCase):
    def setUp(self):
        """
        Set up the test environment.
        """
        self.user = User.objects.create(username="testuser")

    def test_str_representation(self):
        nfc_tag = NFCTag.objects.create(
            serial_number="04E141124C2880",
            integrated_circuit="213",
            user=self.user
        )
        self.assertEqual(str(nfc_tag), "04E141124C2880")

    def test_serial_number_uniqueness(self):
        """
        Testing uniqueness constraint should involve trying to create a second object with the same serial number.
        """
        NFCTag.objects.create(serial_number="04E141124C2880", integrated_circuit="213", user=self.user)
        with self.assertRaises(Exception):  # Adjust the exception type if necessary
            NFCTag.objects.create(serial_number="04E141124C2880", integrated_circuit="213", user=self.user)

    def test_default_values(self):
        nfc_tag = NFCTag.objects.create(
            serial_number="04E141124C2880",
            integrated_circuit="213",
            user=self.user
        )
        self.assertTrue(nfc_tag.active)
        self.assertEqual(nfc_tag.integrated_circuit, "213")

    def test_nullable_user_field(self):
        nfc_tag = NFCTag.objects.create(
            serial_number="04E141124C2880",
            integrated_circuit="213",
            user=None
        )
        self.assertIsNone(nfc_tag.user)
