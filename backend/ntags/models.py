from uuid import uuid4
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse
from wagtail.images import get_image_model
from wagtail.documents import get_document_model
from wagtail.models import (
    DraftStateMixin,
    RevisionMixin,
    LockableMixin,
    TranslatableMixin,
    PreviewableMixin,
    Collection
)
from wagtail.fields import RichTextField

from . import (NTAG213, NTAG_IC_CHOICES)
from .validators import validate_serial_number, validate_integrated_circuit
from .managers import NFCTagManager


class NFCTagType(
    DraftStateMixin,
    RevisionMixin,
    LockableMixin,
    TranslatableMixin,
    PreviewableMixin,
    models.Model
):
    """
    Model representing the type of NFC tag.

    Attributes:
        name (str): The name of the NFC tag type.
        description (str): A description of the NFC tag type.
        collection (ForeignKey): The collection associated with the NFC tag type.
    """
    name = models.CharField(
        max_length=255,
        unique=True
    )
    description = RichTextField(
        null=True
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
        verbose_name = _("nfc tag type")
        verbose_name_plural = _("nfc tag types")


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
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ntags'
    )
    label = models.CharField(
        max_length=64,
        blank=True,
        null=True
    )
    active = models.BooleanField(
        default=True
    )
    nfc_tag_type = models.ForeignKey(
        NFCTagType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ntags'
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ntags'
    )
    object_id = models.PositiveIntegerField(
        null=True,
        blank=True
    )
    content_object = GenericForeignKey(
        'content_type',
        'object_id'
    )

    objects = NFCTagManager()

    @property
    def url(self):
        return self.get_url()

    def get_url(self):
        raise NotImplementedError("Method 'get_url' must be implemented in a subclass.")

    def log_scan(self, counter):
        return NFCTagScan.objects.create(
            ntag=self,
            counter=counter
        )

    def save(self, *args, **kwargs):
        if not self.label:
            if self.user:
                n = self.user.ntags.count() + 1
                self.label = f"NFC Tag {n}"
            else:
                self.label = f"NFC Tag {uuid4()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.serial_number

    class Meta:
        abstract = True
        verbose_name = _("ntag")
        verbose_name_plural = _("ntags")
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


class NFCTag(AbstractNFCTag):

    def get_url(self):
        if self.content_object:
            return self.get_page_url()
        return self.get_edit_url()

    def get_page_url(self):
        if hasattr(self.content_object, 'url'):
            return self.content_object.url

    def get_admin_url(self, action):
        viewset = self.snippet_viewset
        url_name = viewset.get_url_name(action)
        return reverse(url_name, args=[self.pk])

    def get_edit_url(self):
        return self.get_admin_url('edit')

    def get_usage_url(self):
        return self.get_admin_url('usage')


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


class NFCTagScan(models.Model):
    """
    Model representing a scan of an NFC tag.
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
        return f"Scan #{self.counter} for {self.ntag}"

    class Meta:
        verbose_name = _("scan")
        verbose_name_plural = _("scans")
