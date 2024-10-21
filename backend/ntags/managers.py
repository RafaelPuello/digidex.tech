from django.db import models
from django.contrib.contenttypes.models import ContentType

from . import get_nfc_tag_model


class NFCTaggableManager(models.Manager):

    def get_linked_object_type(self):
        """
        Get the ContentType for the linked object.
        """
        return ContentType.objects.get_for_model(self.model)

    def with_nfc_tag(self):
        """
        Get a queryset of linked object instances with NFC tags.
        """
        return self.filter(
            id__in=get_nfc_tag_model().objects.filter(
                content_type=self.get_linked_object_type()
            ).values_list('object_id', flat=True)
        )

    def without_nfc_tag(self):
        """
        Get a queryset of linked object instances without NFC tags.
        """
        return self.exclude(
            id__in=get_nfc_tag_model().objects.filter(
                content_type=self.get_linked_object_type()
            ).values_list('object_id', flat=True)
        )
