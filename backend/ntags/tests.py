from django.contrib.contenttypes.models import ContentType
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
        NFCTag.objects.create(serial_number="04E141124C2880", integrated_circuit="213", user=self.user)
        # Testing uniqueness constraint should involve trying to create a second object with the same serial number.
        with self.assertRaises(Exception):  # Adjust the exception type if necessary
            NFCTag.objects.create(serial_number="04E141124C2880", integrated_circuit="213", user=self.user)

    def test_tagged_items_generic_relation(self):
        nfc_tag = NFCTag.objects.create(
            serial_number="04E141124C2880",
            integrated_circuit="213",
            user=self.user
        )
        content_type = ContentType.objects.get_for_model(NFCTag)
        item = nfc_tag.tagged_items.create(
            content_type=content_type,
            object_id=nfc_tag.id,
            tag="SampleTag"
        )
        self.assertEqual(nfc_tag.tagged_items.count(), 1)
        self.assertEqual(item.tag, "SampleTag")

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
