from uuid import UUID
import pytest
from django.contrib.auth import get_user_model

from ..models import NfcTag, NfcTagType, NfcTagScan

@pytest.mark.django_db
def test_nfc_tag_type_creation():
    tag_type = NfcTagType.objects.create(
        name="Test Tag Type",
        description="A test NFC tag type",
        integrated_circuit=NfcTagType.NTAG213
    )
    assert tag_type.name == "Test Tag Type"
    assert tag_type.description == "A test NFC tag type"
    assert tag_type.integrated_circuit == NfcTagType.NTAG213
    assert tag_type.created_at is not None
    assert tag_type.last_modified is not None
    assert str(tag_type) == "Test Tag Type"

# -------------------------------------------------------------------------------
# ---------------------------- nfc_tag_tests ------------------------------------
# -------------------------------------------------------------------------------

User = get_user_model()

@pytest.mark.django_db
def test_nfc_tag_creation():
    user = User.objects.create_user(username="testuser", password="password")
    tag_type = NfcTagType.objects.create(name="Test Tag Type")
    nfc_tag = NfcTag.objects.create(
        serial_number="04AABBCCDDEEFF",
        nfc_tag_type=tag_type,
        user=user,
        url="https://example.com",
        content={"key": "value"},
        active=True
    )
    assert isinstance(nfc_tag.uuid, UUID)
    assert nfc_tag.serial_number == "04AABBCCDDEEFF"
    assert nfc_tag.nfc_tag_type == tag_type
    assert nfc_tag.user == user
    assert nfc_tag.url == "https://example.com"
    assert nfc_tag.content == {"key": "value"}
    assert nfc_tag.active is True
    assert nfc_tag.created_at is not None
    assert nfc_tag.last_modified is not None
    assert str(nfc_tag) == "NFC Tag: 04:AA:BB:CC:DD:EE:FF"

@pytest.mark.django_db
def test_activate_tag():
    nfc_tag = NfcTag.objects.create(serial_number="04AABBCCDDEEFF", active=False)
    nfc_tag.activate_tag(user=None)
    nfc_tag.refresh_from_db()
    assert nfc_tag.active is True

def test_deactivate_tag():
    nfc_tag = NfcTag.objects.create(serial_number="04AABBCCDDEEFF", active=True)
    nfc_tag.deactivate_tag()
    nfc_tag.refresh_from_db()
    assert nfc_tag.active is False

@pytest.mark.django_db
def test_log_scan():
    user = User.objects.create_user(username="testuser", password="password")
    nfc_tag = NfcTag.objects.create(serial_number="04AABBCCDDEEFF")
    result = nfc_tag.log_scan(user=user, counter="1A")
    assert result is True
    scan = NfcTagScan.objects.get(nfc_tag=nfc_tag)
    assert scan.counter == int("1A", 16)
    assert scan.scanned_by == user

def test_log_scan_invalid_counter():
    nfc_tag = NfcTag(serial_number="04AABBCCDDEEFF")
    result = nfc_tag.log_scan(user=None, counter="ZZ")
    assert result is False

def test_nfc_tag_str_method():
    nfc_tag = NfcTag(serial_number="04AABBCC")
    expected_str = "NFC Tag: 04:AA:BB:CC"
    assert str(nfc_tag) == expected_str

# -------------------------------------------------------------------------------
# ---------------------------- nfc_tag_scan_tests -------------------------------
# -------------------------------------------------------------------------------

@pytest.mark.django_db
def test_nfc_tag_scan_creation():
    user = User.objects.create_user(username="testuser", password="password")
    tag_type = NfcTagType.objects.create(name="Test Tag Type")
    nfc_tag = NfcTag.objects.create(serial_number="04AABBCCDDEEFF", nfc_tag_type=tag_type)
    scan = NfcTagScan.objects.create(
        nfc_tag=nfc_tag,
        counter=1,
        scanned_by=user
    )
    assert scan.nfc_tag == nfc_tag
    assert scan.counter == 1
    assert scan.scanned_by == user
    assert scan.scanned_at is not None
    assert str(scan) == f"Scan of {nfc_tag} by {user} at {scan.scanned_at}"
