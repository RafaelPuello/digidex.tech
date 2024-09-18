import pytest

from nearfieldcommunication.models import NfcTagType

@pytest.mark.django_db
def test_nfc_tag_type_creation():
    tag_type = NfcTagType.objects.create(
        name="Test Tag Type",
        description="A test NFC tag type"
    )
    assert tag_type.name == "Test Tag Type"
    assert tag_type.description == "A test NFC tag type"
    assert tag_type.created_at is not None
    assert tag_type.last_modified is not None
    assert str(tag_type) == "Test Tag Type"
