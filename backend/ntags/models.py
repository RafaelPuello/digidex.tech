from django.db import models, IntegrityError
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
from .validators import validate_ascii_mirror_uid
from .forms import NFCTagAdminForm

User = get_user_model()

NTAG213 = "213"
NTAG215 = "215"
NTAG216 = "216"

NTAG_IC_CHOICES = (
    (NTAG213, "NTAG 213"),
    (NTAG215, "NTAG 215"),
    (NTAG216, "NTAG 216"),
)

NTAG_EEPROM_SIZES = (
    (NTAG213, 180),
    (NTAG215, 540),
    (NTAG216, 924),
)


class BaseNFCTag(models.Model):

    viewset_actions = ['edit', 'usage', 'history']

    limited_options = get_nfc_taggable_models

    serial_number = models.CharField(
        max_length=32,
        editable=False,
        unique=True,
        db_index=True,
        validators=[validate_ascii_mirror_uid]
    )
    integrated_circuit = models.CharField(
        max_length=5,
        choices=NTAG_IC_CHOICES,
        default=NTAG213
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
    metadata = models.JSONField(
        default=dict,
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=_("Content type"),
        limit_choices_to=limited_options,
        null=True,
        blank=True,
        related_name="nfc_tags"
    )
    object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        db_index=True
    )
    content_object = GenericForeignKey(
        "content_type",
        "object_id"
    )


    base_form_class = NFCTagAdminForm

    def __str__(self):
        return f"NFC Tag: {self.serial_number}"

    def __gt__(self, other):
        return self.serial_number > other.serial_number

    def __lt__(self, other):
        return self.serial_number < other.serial_number

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=['content_type', 'object_id'],
                name='unique_content_object'
            )
        ]
        ordering = ['serial_number']
        verbose_name = _("NFC Tag")
        verbose_name_plural = _("NFC Tags")

    def log_scan(self, counter, user=None):
        """
        Log a scan for the NFC tag, optionally including a user.
        """
        scan_data = {
            'nfc_tag': self,
            'counter': self.clean_scan_counter(counter)
        }

        if user:
            if not isinstance(user, User):
                raise TypeError("User must be an instance of User")
            scan_data['scanned_by'] = user

        return self._create_scan_entry(scan_data)

    def _create_scan_entry(self, scan_data):
        """
        Helper method to create the scan entry in the database.
        This handles scan creation and uniqueness constraints.
        """
        try:
            return NFCTagScan.objects.create(**scan_data)
        except IntegrityError:
            raise IntegrityError(_("Scan counter must be unique for each NFC Tag"))

    def clean_scan_counter(self, counter):
        if isinstance(counter, int):
            return counter

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

    def build_context(self):
        return {
            'details': self.get_details()
        }

    def get_details(self):
        _details = {
            'heading': str(self),
            'text': 'Home',
            'url': self.get_fallback_url()
        }

        if self.content_object:
            # An object is tagged
            _details.update({'text': 'View More'})

            try:
                _details.update({'url': self.content_object.url})
            except AttributeError:
                # The object does not have a url method
                pass

        return _details

    @property
    def url(self):
        return self.get_url()

    def get_url(self):
        try:
            obj = self.get_tagged_object()
            return obj.url
        except ValueError or AttributeError:
            return self.get_fallback_url()

    def get_tagged_object(self):
        if not self.content_object:
            raise ValueError("No content object is tagged to this NFC Tag")
        return self.content_object

    @staticmethod
    def get_fallback_url():
        from django.conf import settings
        return settings.NFC_TAG_FALLBACK_URL

    @classmethod
    def get_from_uid(cls, uid):
        try:
            return cls.objects.get(serial_number=uid)
        except cls.DoesNotExist:
            return None


class NFCTag(BaseNFCTag):

    design = models.ForeignKey(
        'NFCTagDesign',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )

    def __str__(self):
        return str(self.content_object) if self.content_object else f"NFC Tag: {self.serial_number}"

    def build_context(self, request):
        context = super().build_context()
        context.update({'views': self.get_views()})
        if self.content_object:
            context.update({'tasks': self.get_tasks(request)})
        return context

    def get_views(self):
        return {action: self.get_admin_url(action) for action in self.viewset_actions}

    def get_tasks(self, request):
        tasks = {}

        try:
            tasks.update(self.content_object.get_inventory_form(request))
        except AttributeError:
            # The object does not have method for tasks
            pass

        return tasks

    def get_admin_url(self, action):
        viewset = self.get_viewset()
        url_name = viewset.get_url_name(action)
        return reverse(url_name, args=[self.pk])

    def get_breadcrumb_items(self):
        viewset = self.get_viewset()
        return viewset.breadcrumbs_items

    def get_viewset(self):
        return self.snippet_viewset


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
        if self.scanned_by:
            return f"{self.nfc_tag} scan #{self.counter} by {self.scanned_by} at {self.scanned_at}"
        return f"{self.nfc_tag} scan #{self.counter} at {self.scanned_at}"

    class Meta:
        verbose_name = _("NFC Tag Scan")
        verbose_name_plural = _("NFC Tag Scans")
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
        verbose_name = _("NFC Tag Design")
        verbose_name_plural = _("NFC Tag Designs")
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
