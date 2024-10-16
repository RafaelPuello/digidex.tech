from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse
from django.contrib.auth import get_user_model
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from base.models import GalleryImageMixin
from . import get_nfc_taggable_models
from .constants import NTAG213, NTAG_IC_CHOICES
from .validators import validate_serial_number, validate_integrated_circuit
from .managers import NFCTagManager

User = get_user_model()


class BaseNFCTag(models.Model):

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
        related_name='nfc_tags'
    )
    active = models.BooleanField(
        default=True
    )
    eeprom = models.JSONField(
        default=dict,
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

    def log_scan(self, counter, user):
        raise NotImplementedError("Method 'log_scan' must be implemented in a subclass.")

    @property
    def url(self):
        return self.get_url()

    def get_url(self):
        raise NotImplementedError("Method 'get_url' must be implemented in a subclass.")


class NFCTag(BaseNFCTag):

    design = models.ForeignKey(
        'NFCTagDesign',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    label = models.CharField(
        max_length=64,
        null=True,
        db_index=True
    )

    def __str__(self):
        if self.label:
            return self.label
        return self.serial_number

    def save(self, *args, **kwargs):
        if not self.label and self.user:
            n = self.user.nfc_tags.count() + 1
            self.label = f"NFC Tag {n}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("nfc-tag")
        verbose_name_plural = _("nfc-tags")
        ordering = ['serial_number']

    def log_scan(self, counter, user=None):
        scan_data = {
            'nfc_tag': self,
            'counter': self.clean_scan_counter(counter)
        }

        if user is not None and isinstance(user, User):
            scan_data['scanned_by'] = user

        try:
            return NFCTagScan.objects.create(**scan_data)
        except Exception as e:
            raise e

    def clean_scan_counter(self, counter):
        if isinstance(counter, int):
            return counter

        # If counter is bytes, decode to a string and convert to int
        elif isinstance(counter, bytes):
            try:
                return int(counter.decode('utf-8'))
            except ValueError:
                raise ValueError("Counter bytes data is not a valid integer")

        elif isinstance(counter, str):
            try:
                return int(counter, 16)  # Convert from hex if necessary
            except ValueError:
                raise ValueError("Counter string data is not a valid integer")

        else:
            raise TypeError("Counter must be an int, bytes, or str")

    def get_tagged_items(self):
        return self.tagged_items.all()

    def get_url(self):
        _object = self.get_tagged_items().first()

        if _object and _object.content_object:
            return self.get_page_url(_object)
        return self.get_edit_url()

    def get_page_url(self, _object):
        if hasattr(_object, 'url'):
            return _object.url

    def get_edit_url(self):
        return self.get_admin_url('edit')

    def get_usage_url(self):
        return self.get_admin_url('usage')

    def get_admin_url(self, action):
        viewset = self.snippet_viewset
        url_name = viewset.get_url_name(action)
        return reverse(url_name, args=[self.pk])


class BaseNFCTaggedItem(models.Model):

    nfc_tag = models.ForeignKey(
        NFCTag,
        related_name="tagged_items",
        on_delete=models.CASCADE
    )
    
    class Meta:
        abstract = True

    def __str__(self):
        return f"Item tagged with NFC Tag: {self.nfc_tag}"


class NFCTaggedItem(BaseNFCTaggedItem):

    limited_options = get_nfc_taggable_models

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=_("Content type"),
        limit_choices_to=limited_options,
        related_name="nfc_tags"
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(
        "content_type",
        "object_id"
    )

    class Meta:
        verbose_name = _("NFC Tagged Item")
        verbose_name_plural = _("NFC Tagged Items")
        constraints = [
            models.UniqueConstraint(
                fields=['content_type', 'object_id', 'nfc_tag'],
                name='unique_content_object'
            )
        ]


class NFCTagScan(models.Model):

    nfc_tag = models.ForeignKey(
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
        return f"Scan #{self.counter} for {self.nfc_tag}"

    class Meta:
        verbose_name = _("scan")
        verbose_name_plural = _("scans")
        constraints = [
            models.UniqueConstraint(
                fields=['nfc_tag', 'counter'], name='unique_nfc_tag_counter'
            )
        ]


class NFCTagDesign(ClusterableModel):

    name = models.CharField(
        max_length=64,
        unique=True
    )
    description = models.TextField(
        blank=True,
        null=True
    )
    designer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='nfc_tag_designs'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("nfc_tag design")
        verbose_name_plural = _("nfc_tag designs")
        ordering = ['name']


class NFCTagDesignGalleryImage(GalleryImageMixin):
    design = ParentalKey(
        NFCTagDesign,
        on_delete=models.CASCADE,
        related_name='gallery_images'
    )

    def get_image_rendition(self, spec):
        """
        Generates an image rendition based on a given spec string
        (e.g., "fill-300x300").
        """
        return self.image.get_rendition(spec)
