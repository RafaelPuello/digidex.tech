import pytest
from django.contrib.auth import get_user_model

from nearfieldcommunication.models import NfcTag, NfcTagType, NfcTagScan, NfcTagMemory

User = get_user_model()

@pytest.mark.django_db
def test_nfc_tag_creation():
    user = User.objects.create_user(username="testuser", password="password")
    tag_type = NfcTagType.objects.create(name="Test Tag Type")
    nfc_tag = NfcTag.objects.create(
        serial_number="04AABBCCDDEEFF",
        nfc_tag_type=tag_type,
        user=user,
        active=True
    )
    assert nfc_tag.serial_number == "04AABBCCDDEEFF"
    assert nfc_tag.nfc_tag_type == tag_type
    assert nfc_tag.user == user
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
