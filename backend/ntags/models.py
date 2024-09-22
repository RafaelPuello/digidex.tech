from uuid import uuid4
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from .constants import NTAG213, IC_CHOICES, EEPROM_SIZE
from .validators import validate_serial_number, validate_integrated_circuit
from .utils import get_nfc_tag_model, get_nfc_tag_model_string


class NFCTaggableManager(models.Manager):
    def add(self, obj, nfc_tag):
        content_type = ContentType.objects.get_for_model(obj)
        tagged_item, created = NFCTaggedItem.objects.get_or_create(
            nfc_tag=nfc_tag,
            content_type=content_type,
            object_id=obj.pk
        )
        return tagged_item

    def remove(self, obj, nfc_tag):
        content_type = ContentType.objects.get_for_model(obj)
        return NFCTaggedItem.objects.filter(
            nfc_tag=nfc_tag,
            content_type=content_type,
            object_id=obj.pk
        ).delete()

    def clear(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return NFCTaggedItem.objects.filter(
            content_type=content_type,
            object_id=obj.pk
        ).delete()

    def get_tags(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return NFCTag.objects.filter(
            tagged_items__content_type=content_type,
            tagged_items__object_id=obj.pk
        )


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

    def add(self, *tags):
        NFCTag = get_nfc_tag_model()
        for tag in tags:
            if not isinstance(tag, NFCTag):
                raise ValueError("All tags must be instances of the NFCTag model.")
            NFCTaggedItem.objects.create(
                nfc_tag=tag,
                content_object=self.instance
            )

    def remove(self, *tags):
        NFCTaggedItem.objects.filter(
            nfc_tag__in=tags,
            content_type=ContentType.objects.get_for_model(self.instance),
            object_id=self.instance.pk
        ).delete()

    def clear(self):
        NFCTaggedItem.objects.filter(
            content_type=ContentType.objects.get_for_model(self.instance),
            object_id=self.instance.pk
        ).delete()

    def all(self):
        NFCTag = get_nfc_tag_model()
        return NFCTag.objects.filter(
            tagged_items__content_type=ContentType.objects.get_for_model(self.instance),
            tagged_items__object_id=self.instance.pk
        )


class AbstractNFCTag(models.Model):
    """
    Abstract base model for NFCTag.
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
    active = models.BooleanField(
        default=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ntags'
    )
    tagged_items = GenericRelation(
        'NFCTaggedItem'
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
        pass

    def __str__(self):
        return self.serial_number

    class Meta:
        abstract = True
        verbose_name = _("ntag")
        verbose_name_plural = _("ntags")


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
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    last_modified = models.DateTimeField(
        auto_now=True
    )

    @classmethod
    def get_for_ntag(cls, ntag):
        """
        Gets or creates the EEPROM object for the NFC tag.
        """
        columns = 4
        rows = EEPROM_SIZE[ntag.integrated_circuit] // columns

        # Create a 2D NumPy array filled with zeros
        eeprom_2d = None #  np.zeros((rows, columns), dtype=np.uint8)
        eeprom_bytes = eeprom_2d.tobytes()

        ntag_eeprom = cls.objects.create(
            ntag=ntag,
            eeprom=eeprom_bytes
        )
        cls.objects.get_or_create(ntag=ntag)
        return ntag_eeprom, eeprom_2d.view()


    def __str__(self):
        return str(self.ntag)

    class Meta:
        verbose_name = _("eeprom")
        verbose_name_plural = _("eeproms")


class NFCTag(AbstractNFCTag):
    """
    Default concrete NFCTag model.
    """

    pass


class NFCTaggedItem(models.Model):
    """
    Model representing the relationship between NFCTags and any other model instance.
    """

    nfc_tag = models.ForeignKey(
        get_nfc_tag_model_string(),
        on_delete=models.CASCADE,
        related_name='tagged_items'
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name='nfc_tagged_items'
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(
        'content_type',
        'object_id'
    )

    class Meta:
        unique_together = ('nfc_tag', 'content_type', 'object_id')
        verbose_name = _("NFC Tagged Item")
        verbose_name_plural = _("NFC Tagged Items")

    def __str__(self):
        return f"{self.nfc_tag} tagged to {self.content_object}"


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
        return (f"Scan #{self.counter} for {self.ntag}")

    class Meta:
        verbose_name = _("scan")
        verbose_name_plural = _("scans")
