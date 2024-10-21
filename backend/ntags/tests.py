from django.test import TestCase

from .models import NFCTag


class NFCTagModelTest(TestCase):
    def setUp(self):
        """
        Set up the test environment.
        """
        pass

    def test_uid_uniqueness(self):
        """
        Testing uniqueness constraint should involve trying to create a second object with the same serial number.
        """
        NFCTag.objects.create(uid="04E141124C2880", integrated_circuit="213")
        with self.assertRaises(Exception):
            NFCTag.objects.create(uid="04E141124C2880", integrated_circuit="213")
