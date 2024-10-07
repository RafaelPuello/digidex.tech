from django.db import models
from django.utils.translation import gettext_lazy as _

from . import get_nfc_tag_filter_method


class NFCTagManager(models.Manager):
    def __init__(self, through=None, model=None, instance=None):
        self.through = through
        self.model = model
        self.instance = instance
        super().__init__()

    def __get__(self, instance, model):
        manager = NFCTagManager(
            through=self.through,
            model=self.model,
            instance=instance
        )
        return manager

    def get_from_mirror(self, ascii_mirror, user=None):
        """
        Retrieves an NFCTag instance based on the mirrored ASCII value and filter type.
        """
        ntag_filter = get_nfc_tag_filter_method()

        if ntag_filter == 'uid':
            return self.get_from_uid(ascii_mirror)
        elif ntag_filter == 'uid_counter':
            return self.get_from_uid_counter(ascii_mirror, user)
        else:
            raise ValueError(_('Invalid filter method.'))

    def get_from_uid(self, uid):
        """
        Retrieves an NFCTag instance based on the UID.
        """
        try:
            return self.get(serial_number=uid)
        except self.model.DoesNotExist:
            raise self.model.DoesNotExist(_('NFC Tag not found.'))

    def get_from_uid_counter(self, uid_counter, user=None):
        """
        Retrieves an NFCTag instance based on the UID and counter.
        """
        if 'x' not in uid_counter:
            raise ValueError(_('Invalid NFC Tag Mirror.'))
        uid, counter = uid_counter.split('x')

        try:
            ntag = self.get(serial_number=uid)
            if user:
                ntag.log_scan(counter, user)
            return ntag
        except self.model.DoesNotExist:
            raise self.model.DoesNotExist(_('NFC Tag Scan not found.'))
