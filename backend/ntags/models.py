from uuid import uuid4
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from . import (
    get_nfc_tag_model_string,
    NTAG213, NTAG_IC_CHOICES, NTAG_EEPROM_SIZES
)
from .validators import validate_serial_number, validate_integrated_circuit
from .managers import NFCTagManager


class AbstractNFCTag(models.Model):
    """
    Abstract base model for NFC Tags.
    """
    serial_number = models.CharField(
        max_length=32,
        editable=False,
        unique=True,
        db_index=True,
        validators=[validate_serial_number]
    )
    integrated_circuit = models.CharField(
        max_length=5,
        choices=NTAG_IC_CHOICES,
        default=NTAG213,
        validators=[validate_integrated_circuit]
    )
    active = models.BooleanField(default=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ntags'
    )

    objects = NFCTagManager()

    def log_scan(self, counter):
        from .models import NFCTagScan
        return NFCTagScan.objects.create(
            ntag=self,
            counter=counter
        )

    def __str__(self):
        return self.serial_number

    class Meta:
        abstract = True
        verbose_name = _("ntag")
        verbose_name_plural = _("ntags")


class NFCTag(AbstractNFCTag):
    """
    Concrete model for NFC Tags.
    """
    pass


class NFCTagMemory(models.Model):
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
        verbose_name = _("eeprom")
        verbose_name_plural = _("eeproms")



class NFCTagScan(models.Model):
    """
    Model representing a scan of an NFC tag.
    """
    ntag = models.ForeignKey(
        get_nfc_tag_model_string(),
        on_delete=models.CASCADE,
        related_name='scans'
    )
    counter = models.PositiveIntegerField(
        validators=[MinValueValidator(0)]
    )
    scanned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='+'
    )
    scanned_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Scan #{self.counter} for {self.ntag}"

    class Meta:
        verbose_name = _("scan")
        verbose_name_plural = _("scans")
