from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..constants import NTAG_EEPROM_SIZES
from ..utils import get_nfc_tag_model_string


class AbstractNFCTagMemory(models.Model):
    """
    Model representing the EEPROM contents of an NFC tag.
    """

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        unique=True,
    )
    ntag = models.OneToOneField(
        get_nfc_tag_model_string(),
        on_delete=models.CASCADE,
        related_name='eeprom'
    )
    eeprom = models.BinaryField(
        max_length=888,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    @classmethod
    def get_for_ntag(cls, ntag):
        """
        Retrieves or creates the EEPROM object for the given NFC tag.
        """

        columns = 4
        rows = NTAG_EEPROM_SIZES[ntag.integrated_circuit] // columns

        # Create a 2D NumPy array filled with zeros (assuming NumPy is used)
        eeprom_2d = None #  np.zeros((rows, columns), dtype=np.uint8)
        eeprom_bytes = eeprom_2d.tobytes()

        ntag_eeprom, created = cls.objects.get_or_create(
            ntag=ntag,
            defaults={'eeprom': eeprom_bytes}
        )
        return ntag_eeprom, eeprom_2d.view()

    def __str__(self):
        return str(self.ntag)

    class Meta:
        abstract = True
        verbose_name = _("eeprom")
        verbose_name_plural = _("eeproms")


class NFCTagMemory(AbstractNFCTagMemory):
    pass
