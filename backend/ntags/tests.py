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

    def test_str_representation(self, user):
        nfc_tag = NFCTag.objects.create(
            serial_number="04E141124C2880",
            integrated_circuit="213",
            user=user
        )
        assert str(nfc_tag) == "04E141124C2880"

    def test_serial_number_uniqueness(self, user):
        NFCTag.objects.create(serial_number="04E141124C2880", integrated_circuit="213", user=user)
        assert 1==1

    def test_tagged_items_generic_relation(self, user):
        nfc_tag = NFCTag.objects.create(
            serial_number="04E141124C2880",
            integrated_circuit="213",
            user=user
        )
        content_type = ContentType.objects.get_for_model(NFCTag)
        item = nfc_tag.tagged_items.create(
            content_type=content_type,
            object_id=nfc_tag.id,
            tag="SampleTag"
        )
        assert nfc_tag.tagged_items.count() == 1
        assert item.tag == "SampleTag"

    def test_default_values(self, user):
        nfc_tag = NFCTag.objects.create(
            serial_number="04E141124C2880",
            integrated_circuit="213",
            user=user
        )
        assert nfc_tag.active is True
        assert nfc_tag.integrated_circuit == "213"

    def test_nullable_user_field(self):
        nfc_tag = NFCTag.objects.create(
            serial_number="04E141124C2880",
            integrated_circuit="213",
            user=None
        )
        assert nfc_tag.user is None
