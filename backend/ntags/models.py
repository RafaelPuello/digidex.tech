from django.db import models, IntegrityError
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse
from django.contrib.auth import get_user_model

from . import get_nfc_taggable_models, get_nfc_tag_fallback_url
from .validators import validate_ascii_mirror_uid
from .forms import NFCTagForm, NFCTagRegistrationForm

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


class AbstractNFCTag(models.Model):

    uid = models.CharField(
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

    def __str__(self):
        return f"NFC Tag: {self.uid}"

    def __gt__(self, other):
        return self.uid > other.uid

    def __lt__(self, other):
        return self.uid < other.uid

    class Meta:
        abstract = True
        ordering = ['uid']
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
        context = {}

        if self.user:
            context.update({'details': self.get_details()})
        else:
            context.update({'form': self.get_form()})

        return context

    def get_details(self):
        return {
            'heading': str(self),
            'text': 'Home',
            'url': self.get_fallback_url()
        }

    def get_form(self):
        form = {} 

        if not self.user:
            form.update({'register': NFCTagRegistrationForm()})

        return form

    @property
    def url(self):
        return self.get_url()

    def get_url(self):
        return self.get_fallback_url()

    def get_fallback_url(self):
        return get_nfc_tag_fallback_url()


class BaseNFCTag(AbstractNFCTag):

    viewset_actions = ['edit', 'usage', 'history']

    class Meta(AbstractNFCTag.Meta):
        abstract = True

    def build_context(self, request):
        context = super().build_context()
        return context.update({'views': self.get_views(request.user)})

    def get_views(self, user):
        actions = []

        if not self.user:
            actions.append('register')

        elif self.user == user:
            actions.append(self.viewset_actions)

        return {action: self.get_admin_url(action) for action in actions}

    def get_admin_url(self, action):
        if action == 'register':
            return reverse('ntags:register_nfc_tag', args=[self.pk])

        viewset = self.get_viewset()
        url_name = viewset.get_url_name(action)
        return reverse(url_name, args=[self.pk])

    def get_breadcrumb_items(self):
        viewset = self.get_viewset()
        return viewset.breadcrumbs_items

    def get_viewset(self):
        return self.snippet_viewset


class BaseGenericNFCTag(BaseNFCTag):

    limited_options = get_nfc_taggable_models

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

    base_form_class = NFCTagForm

    def __str__(self):
        return f"NFC link for {str(self.content_object)}" if self.content_object else f"NFC Tag: {self.uid}"

    class Meta(BaseNFCTag.Meta):
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=['content_type', 'object_id'],
                name='unique_content_object'
            )
        ]

    def build_context(self, request):
        context = super().build_context(request)

        if self.content_object:
            context.update({'forms': self.get_form(request)})

        return context

    def get_form(self, request):
        form = super().get_form()

        try:
            form.update(self.content_object.get_inventory_form(request))
        except AttributeError:  # The object does not have method for forms
            pass

        return form

    def get_details(self):
        details = super().get_details()

        if self.content_object:  # Check if the NFC Tag is tagged to an object
            details.update({'text': 'View More'})

            try:  # The object does not have a url attribute or property
                details.update({'url': self.content_object.url})
            except AttributeError:
                pass

        return details

    def get_url(self):
        if self.content_object:
            try:
                return self.content_object.url
            except AttributeError:  # The object does not have an attribute or property for url
                return super().get_url()


class NFCTag(BaseGenericNFCTag):

    class Meta(BaseGenericNFCTag.Meta):
        pass


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
