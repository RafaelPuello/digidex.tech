import pytest
from django.contrib.auth import get_user_model

from nearfieldcommunication.models import NfcTag, NfcTagType, NfcTagScan

User = get_user_model()

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
