import uuid
import numpy as np
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from wagtail.models import (
    Collection,
    RevisionMixin,
    DraftStateMixin,
    LockableMixin,
    TranslatableMixin,
    PreviewableMixin
)
from wagtail.fields import RichTextField
from wagtail.images import get_image_model
from wagtail.documents import get_document_model

from .constants import NTAG213, IC_CHOICES, EEPROM_SIZE
from .validators import validate_serial_number, validate_integrated_circuit


class NFCTagDesign(
    DraftStateMixin,
    RevisionMixin,
    LockableMixin,
    TranslatableMixin,
    PreviewableMixin,
    models.Model
):
    """
    Model representing the design of an ntag.

    Attributes:
        name (str): The name of the ntag design.
        description (str): A description of the ntag design.
        designer (ForeignKey): The user who designed the ntag.
        uuid (UUID): A unique identifier for the ntag design.
        collection (ForeignKey): The collection associated with the ntag design.
    """
    name = models.CharField(
        max_length=255,
        unique=True
    )
    description = RichTextField(
        null=True
    )
    designer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='designs',
        null=True
    )
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True
    )
    collection = models.ForeignKey(
        Collection,
        on_delete=models.SET_NULL,
        related_name='+',
        null=True,
        blank=True
    )

    def get_documents(self):
        return get_document_model().objects.filter(collection=self.collection)

    def get_images(self):
        return get_image_model().objects.filter(collection=self.collection)

    def __str__(self):
        return self.name

    class Meta(TranslatableMixin.Meta):
        verbose_name = _("design")
        verbose_name_plural = _("designs")


class NFCTag(models.Model):
    """
    Model representing an individual ntag, which is linked to a physical object.

    Attributes:
        serial_number (str): The serial number of the NFC tag.
        integrated_circuit (str): The type of integrated circuit used in the NFC tag.
        user (User): The user who is assigned the NFC tag.
        design (NfcTagDesign): The design of NFC tag.
        active (bool): Indicates whether the NFC tag is active.
        content (json): The content stored on the NFC tag.
        created_at (datetime): The date and time when the NFC tag was created.
        last_modified (datetime): The date and time when the NFC tag was last modified.
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
        choices=IC_CHOICES,
        default=NTAG213,
        validators=[validate_integrated_circuit]
    )
    design = models.ForeignKey(
        NFCTagDesign,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='ntags'
    )
    active = models.BooleanField(
        default=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='ntags'
    )
    content = models.JSONField(
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    last_modified = models.DateTimeField(
        auto_now=True
    )

    def create_eeprom(self):
        """
        Creates and returns a new eeprom object for the NFC tag.
        """
        columns = 4
        rows = EEPROM_SIZE[self.integrated_circuit] // columns

        # Create a 2D NumPy array filled with zeros
        eeprom_2d = np.zeros((rows, columns), dtype=np.uint8)
        eeprom_bytes = eeprom_2d.tobytes()

        ntag_eeprom = NFCTagEEPROM.objects.create(
            ntag=self,
            eeprom=eeprom_bytes
        )
        return ntag_eeprom, eeprom_2d.view()

    def log_scan(self, user, counter):
        """
        Logs a scan of the NFC tag, storing the counter and user who scanned it.

        Args:
            user (User): The user who scanned the NFC tag.
            counter (int or str): The scan counter, which can be an integer or a hexadecimal string.

        Returns:
            bool: True if the scan was logged successfully, False otherwise.
        """
        try:
            cnt = int(counter, 16) if isinstance(counter, str) else int(counter)
            NFCTagScan.objects.create(
                ntag=self,
                counter=cnt,
                scanned_by=user
            )
            return True
        except (ValueError, TypeError) as e:
            print(f"Error logging scan: {e}")
            return False

    def activate_tag(self):
        """
        Activates the NFC tag.
        """
        self.active = True
        self.save()

    def deactivate_tag(self):
        """
        Deactivates the NFC tag.
        """
        self.active = False
        self.save()

    def __str__(self):
        return self.serial_number

    class Meta:
        verbose_name = _("ntag")
        verbose_name_plural = _("ntags")


class NFCTagScan(models.Model):
    """
    Model representing a scan of an NFC tag.

    Attributes:
        ntag (NfcTag): The NFC tag that was scanned.
        counter (int): The scan counter value.
        scanned_by (User): The user who scanned the NFC tag.
        scanned_at (datetime): The date and time when the NFC tag was scanned.
    """

    ntag = models.ForeignKey(
        NFCTag,
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
        return (f"Scan #{self.counter} for {self.ntag}")

    class Meta:
        verbose_name = _("scan")
        verbose_name_plural = _("scans")


class NFCTagEEPROM(models.Model):
    """
    Model representing the eeprom contents of an NFC tag.

    Attributes:
        uuid (UUID): A unique identifier for the NFC tag.
        ntag (NfcTag): The NFC tag whose eeprom contents are stored.
        eeprom (binary): The eeprom contents of the NFC tag.
        created_at (datetime): The date and time when the eeprom contents were created.
        last_modified (datetime): The date and time when the eeprom contents were last modified.
    """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    ntag = models.OneToOneField(
        NFCTag,
        on_delete=models.CASCADE,
        related_name='eeprom'
    )
    eeprom = models.BinaryField(
        max_length=888,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    last_modified = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return str(self.ntag)

    class Meta:
        verbose_name = _("eeprom")
        verbose_name_plural = _("eeproms")
