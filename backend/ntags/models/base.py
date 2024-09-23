from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

from ..constants import NTAG213, NTAG_IC_CHOICES
from ..validators import validate_serial_number, validate_integrated_circuit
from ..utils import get_nfc_tag_model, get_nfc_tag_model_string, get_nfc_tag_filter_method, get_nfc_tag_scan_model


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

    def get_from_mirror(self, ascii_mirror):
        """
        Retrieves an NFCTag instance based on the mirrored ASCII value and filter type.
        """

        if not ascii_mirror:
            raise ValueError(_('Invalid NFC tag URI.'))

        ntag_filter = get_nfc_tag_filter_method()

        if ntag_filter == 'uid':
            return self.get_from_uid(ascii_mirror)

        elif ntag_filter == 'counter':
            return self.get_from_counter(ascii_mirror)

        elif ntag_filter == 'uid_counter':
            return self.get_from_uid_counter(ascii_mirror)

        else:
            raise ValueError(_('Invalid filter method.'))

    def get_from_uid(self, uid):
        """
        Retrieves an NFCTag instance based on the UID.
        """

        try:
            return self.get(serial_number=uid)

        except self.model.DoesNotExist:
            raise self.model.DoesNotExist(_('NFC Tag not found.'))

    def get_from_counter(self, counter):
        """
        Retrieves an NFCTag instance based on the Counter.
        """

        latest_scan_subquery = get_nfc_tag_scan_model().objects.filter(
            ntag=models.OuterRef('pk')
        ).order_by('-scanned_at').values('counter')[:1]

        # Annotate NFCTag with the latest counter value
        queryset = self.annotate(
            latest_counter=models.Subquery(latest_scan_subquery)
        ).filter(
            latest_counter=counter
        )

        return queryset

    def get_from_uid_counter(self, uid_counter):
        """
        Retrieves an NFCTag instance based on the UID and counter.
        """

        if 'x' not in uid_counter:
            raise ValueError(_('Invalid NFC Tag Mirror.'))
        uid, counter = uid_counter.split('x')

        try:
            return self.get(serial_number=uid).scans.get(counter=counter)
        except self.model.DoesNotExist:
            raise self.model.DoesNotExist(_('NFC Tag Scan not found.'))

    def add(self, *ntags):
        NFCTag = get_nfc_tag_model()
        for ntag in ntags:
            if not isinstance(ntag, NFCTag):
                raise ValueError("All NFC-Tags must be instances of the NFCTag model.")
            NFCTaggedItem.objects.create(
                nfc_tag=ntag,
                content_object=self.instance
            )

    def remove(self, *ntags):
        NFCTaggedItem.objects.filter(
            nfc_tag__in=ntags,
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
    tagged_items = GenericRelation('NFCTaggedItem')

    def log_scan(self, counter):
        return get_nfc_tag_scan_model().objects.create(
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
    pass


class BaseNFCTaggableManager(models.Manager):
    """
    Manager to handle NFC tag associations with arbitrary models.
    Provides methods to add, remove, clear tags associated with an object,
    and retrieve tags associated with an object.
    """

    def add(self, obj, ntag):
        content_type = ContentType.objects.get_for_model(obj)
        tagged_item, created = NFCTaggedItem.objects.get_or_create(
            nfc_tag=ntag,
            content_type=content_type,
            object_id=obj.pk
        )
        return tagged_item

    def remove(self, obj, ntag):
        content_type = ContentType.objects.get_for_model(obj)
        return NFCTaggedItem.objects.filter(
            nfc_tag=ntag,
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
        NFCTag = get_nfc_tag_model()
        content_type = ContentType.objects.get_for_model(obj)
        return NFCTag.objects.filter(
            tagged_items__content_type=content_type,
            tagged_items__object_id=obj.pk
        )


class NFCTaggedItem(models.Model):
    """
    Model representing the relationship between NFC tags and any other model instance.
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
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.nfc_tag} tagged to {self.content_object}"

    class Meta:
        unique_together = ('nfc_tag', 'content_type', 'object_id')
        verbose_name = _("NFC Tagged Item")
        verbose_name_plural = _("NFC Tagged Items")
