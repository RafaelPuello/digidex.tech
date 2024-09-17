import uuid
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from .validators import validate_serial_number


NTAG213 = "213"
NTAG215 = "215"
NTAG216 = "216"

IC_CHOICES = (
    (NTAG213, _("NTAG 213")),
    (NTAG215, _("NTAG 215")),
    (NTAG216, _("NTAG 216")),
)

MEMORY_SIZE = {
    NTAG213: 144,
    NTAG215: 504,
    NTAG216: 888,
}

class NfcTagType(models.Model):
    """
    Model representing the type of NFC tag.
    
    Attributes:
        name (str): The name of the NFC tag type.
        description (str): A description of the NFC tag type.
        created_at (datetime): The date and time when the tag type was created.
        last_modified (datetime): The date and time when the tag type was last modified.
    """

    name = models.CharField(
        max_length=255,
        unique=True
    )
    description = models.TextField(
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    last_modified = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        """
        Returns a string representation of the NFC tag type.
        """
        return self.name

    class Meta:
        verbose_name = _("nfc tag type")
        verbose_name_plural = _("nfc tag types")


class NfcTag(models.Model):
    """
    Model representing an individual NFC tag, which is linked to a physical object.
    
    Attributes:
        uuid (UUID): A unique identifier for the NFC tag.
        serial_number (str): The serial number of the NFC tag.
        user (User): The user who is assigned the NFC tag.
        nfc_tag_type (NfcTagType): The type of NFC tag.
        url (URL): The URL associated with the NFC tag.
        active (bool): Indicates whether the NFC tag is active.
        created_at (datetime): The date and time when the NFC tag was created.
        last_modified (datetime): The date and time when the NFC tag was last modified.
    """

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    serial_number = models.CharField(
        max_length=32,
        editable=False,
        unique=True,
        db_index=True,
        validators=[validate_serial_number]
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='tags'
    )
    nfc_tag_type = models.ForeignKey(
        NfcTagType,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='tags'
    )
    url = models.URLField(
        null=True
    )
    active = models.BooleanField(
        default=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    last_modified = models.DateTimeField(
        auto_now=True
    )

    def create_memory(self, ic_type=NTAG213):
        """
        Creates a new memory object for the NFC tag.

        Args:
            ic_type (str): The type of integrated circuit used in the NFC tag.
            memory (binary): The memory contents of the NFC tag.
        
        Returns:
            NfcTagMemory: The newly created memory object.
        """
    
        if ic_type not in dict(IC_CHOICES).keys():
            raise ValueError(_("Invalid integrated circuit type."))
        
        # Initialize memory with zeros
        memory = b'\x00' * MEMORY_SIZE[ic_type]

        return NfcTagMemory.objects.create(
            nfc_tag=self,
            integrated_circuit=ic_type,
            memory=memory
        )

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
            NfcTagScan.objects.create(
                nfc_tag=self,
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
        """
        Returns a string representation of the NFC tag, with the serial number formatted as pairs of characters.
        """
        uid = ':'.join(self.serial_number[i:i+2] for i in range(0, len(self.serial_number), 2))
        if self.nfc_tag_type:
            return str(f"{self.nfc_tag_type}: {uid}")
        return str(uid)

    class Meta:
        verbose_name = _("nfc tag")
        verbose_name_plural = _("nfc tags")


class NfcTagScan(models.Model):
    """
    Model representing a scan of an NFC tag.
    
    Attributes:
        nfc_tag (NfcTag): The NFC tag that was scanned.
        counter (int): The scan counter value.
        scanned_by (User): The user who scanned the NFC tag.
        scanned_at (datetime): The date and time when the NFC tag was scanned.
    """

    nfc_tag = models.ForeignKey(
        NfcTag,
        on_delete=models.CASCADE,
        related_name='scans'
    )
    counter = models.PositiveIntegerField(
        validators=[MinValueValidator(0)]
    )
    scanned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='scans'
    )
    scanned_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        """
        Returns a string representation of the NFC tag scan, including the scanning user and timestamp if available.
        """
        if self.scanned_by:
            return str(_(f"Scan of {self.nfc_tag} by {self.scanned_by} at {self.scanned_at}"))
        return str(_(f"Scan of {self.nfc_tag} at {self.scanned_at}"))

    class Meta:
        verbose_name = _("nfc tag scan")
        verbose_name_plural = _("nfc tag scans")


class NfcTagMemory(models.Model):
    """
    Model representing the memory contents of an NFC tag.
    
    Attributes:
        nfc_tag (NfcTag): The NFC tag whose memory contents are stored.
        integrated_circuit (str): The type of integrated circuit used in the NFC tag.
        memory (binary): The memory contents of the NFC tag.
        created_at (datetime): The date and time when the memory contents were created.
        last_modified (datetime): The date and time when the memory contents were last modified.
    """

    nfc_tag = models.OneToOneField(
        NfcTag,
        on_delete=models.CASCADE,
        related_name='memory'
    )
    integrated_circuit = models.CharField(
        max_length=5,
        choices=IC_CHOICES,
        default=NTAG213,
    )
    memory = models.BinaryField(
        max_length=888,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    last_modified = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        """
        Returns a string representation of the NFC tag memory contents.
        """
        return str(self.nfc_tag)

    class Meta:
        verbose_name = _("nfc tag memory")
        verbose_name_plural = _("nfc tag memory")
