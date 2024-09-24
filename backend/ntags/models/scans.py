from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from ..utils import get_nfc_tag_model_string


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
        abstract = True
        verbose_name = _("scan")
        verbose_name_plural = _("scans")
