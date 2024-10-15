from uuid import uuid4
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse
from django.contrib.auth import get_user_model

from . import get_nfc_taggable_models
from .constants import NTAG213, NTAG_IC_CHOICES
from .validators import validate_serial_number, validate_integrated_circuit
from .managers import NFCTagManager

User = get_user_model()


class BaseNFCTag(models.Model):

    limited_options = get_nfc_taggable_models

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
        editable=False,
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
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to=limited_options,
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

    def __str__(self):
        return self.serial_number

    def __gt__(self, other):
        return self.serial_number > other.serial_number

    def __lt__(self, other):
        return self.serial_number < other.serial_number

    class Meta:
        abstract = True
        verbose_name = _("ntag")
        verbose_name_plural = _("ntags")
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def save(self, *args, **kwargs):
        if not self.label:
            if self.user:
                n = self.user.ntags.count() + 1
                self.label = f"NFC Tag {n}"
            else:
                self.label = f"NFC Tag {uuid4()}"
        super().save(*args, **kwargs)

    def log_scan(self, counter, user):
        raise NotImplementedError("Method 'log_scan' must be implemented in a subclass.")

    @property
    def url(self):
        return self.get_url()

    def get_url(self):
        raise NotImplementedError("Method 'get_url' must be implemented in a subclass.")


class NFCTag(BaseNFCTag):

    def log_scan(self, counter, user=None):
        scan_data = {
            'ntag': self,
            'counter': counter
        }

        if user is not None and isinstance(user, User):
            scan_data['scanned_by'] = user

        try:
            return NFCTagScan.objects.create(**scan_data)
        except Exception as e:
            raise e


    def get_url(self):
        if self.content_object:
            return self.get_page_url()
        return self.get_edit_url()

    def get_page_url(self):
        if hasattr(self.content_object, 'url'):
            return self.content_object.url

    def get_edit_url(self):
        return self.get_admin_url('edit')

    def get_usage_url(self):
        return self.get_admin_url('usage')

    def get_admin_url(self, action):
        viewset = self.snippet_viewset
        url_name = viewset.get_url_name(action)
        return reverse(url_name, args=[self.pk])


class NFCTagMemory(models.Model):

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
        max_length=924,
    )

    def __str__(self):
        return str(self.ntag)

    class Meta:
        verbose_name = _("eeprom")
        verbose_name_plural = _("eeproms")


class NFCTagScan(models.Model):

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
        constraints = [
            models.UniqueConstraint(
                fields=['ntag', 'counter'], name='unique_ntag_counter'
            )
        ]
