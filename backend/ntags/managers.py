from django.db import models
from django.utils.translation import gettext_lazy as _

from .utils import get_nfc_tag_filter_method


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

    def get_from_mirror(self, ascii_mirror):
        """
        Retrieves an NFCTag instance based on the mirrored ASCII value and filter type.
        """
        if not ascii_mirror:
            raise ValueError(_('Invalid NFC tag URI.'))

        ntag_filter = get_nfc_tag_filter_method()

        if ntag_filter == 'uid':
            return self.get_from_uid(ascii_mirror)
        elif ntag_filter == 'counter':
            return self.get_from_counter(ascii_mirror)
        elif ntag_filter == 'uid_counter':
            return self.get_from_uid_counter(ascii_mirror)
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

    def get_from_counter(self, counter):
        """
        Retrieves an NFCTag instance based on the Counter.
        """
        from .models import NFCTagScan
        latest_scan_subquery = NFCTagScan.objects.filter(
            ntag=models.OuterRef('pk')
        ).order_by('-scanned_at').values('counter')[:1]

        # Annotate NFCTag with the latest counter value
        queryset = self.annotate(
            latest_counter=models.Subquery(latest_scan_subquery)
        ).filter(
            latest_counter=counter
        )
        return queryset

    def get_from_uid_counter(self, uid_counter):
        """
        Retrieves an NFCTag instance based on the UID and counter.
        """
        if 'x' not in uid_counter:
            raise ValueError(_('Invalid NFC Tag Mirror.'))
        uid, counter = uid_counter.split('x')

        try:
            return self.get(serial_number=uid).scans.get(counter=counter)
        except self.model.DoesNotExist:
            raise self.model.DoesNotExist(_('NFC Tag Scan not found.'))
