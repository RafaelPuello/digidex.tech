from rest_framework import serializers
from wagtail.images.api.fields import ImageRenditionField
from wagtail.documents.api.v2.serializers import DocumentDownloadUrlField

from .models import NfcTagType, NfcTagTypeImage, NfcTagTypeDocument, NfcTag, NfcTagScan, NfcTagMemory


class NfcTagTypeImageSerializer(serializers.ModelSerializer):
    """
    Serializer for the NfcTagTypeImage model, representing images associated with an NFC tag type.
    Uses Wagtail's ImageRenditionField to generate image renditions.
    """

    image = ImageRenditionField('fill-800x800')

    class Meta:
        model = NfcTagTypeImage
        fields = ['id', 'image', 'caption', 'sort_order']


class NfcTagTypeDocumentSerializer(serializers.ModelSerializer):
    """
    Serializer for the NfcTagTypeDocument model, representing documents associated with an NFC tag type.
    Uses Wagtail's DocumentDownloadUrlField to generate download links for the documents.
    """

    document = DocumentDownloadUrlField()

    class Meta:
        model = NfcTagTypeDocument
        fields = ['id', 'document', 'caption', 'sort_order']


class NfcTagTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for the NfcTagType model. It includes nested serializers for images and documents 
    related to the NFC tag type.
    """

    images = NfcTagTypeImageSerializer(many=True)
    documents = NfcTagTypeDocumentSerializer(many=True)

    class Meta:
        model = NfcTagType
        fields = ['id', 'name', 'description', 'images', 'documents']


class NfcTagScanSerializer(serializers.ModelSerializer):
    """
    Serializer for the NfcTagScan model, representing scans of an NFC tag.
    It includes information about the scan counter, the user who scanned, and the timestamp.
    """

    scanned_by = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = NfcTagScan
        fields = ['id', 'nfc_tag', 'counter', 'scanned_by', 'scanned_at']


class NfcTagMemorySerializer(serializers.ModelSerializer):
    """
    Serializer for the NfcTagMemory model, representing the memory contents of an NFC tag.
    Includes details about the memory content, the integrated circuit type, and timestamps.
    """

    class Meta:
        model = NfcTagMemory
        fields = ['uuid', 'nfc_tag', 'integrated_circuit', 'memory', 'created_at', 'last_modified']


class NfcTagSerializer(serializers.ModelSerializer):
    """
    Main serializer for the NfcTag model. It includes related scans and memory contents, 
    as well as information about the associated content object through the GenericForeignKey.
    """

    content_object = serializers.SerializerMethodField()
    scans = NfcTagScanSerializer(many=True, read_only=True)
    memory = NfcTagMemorySerializer(read_only=True)

    def get_content_object(self, obj):
        """
        Dynamically retrieves the object represented by the GenericForeignKey. This function can 
        be extended to handle various content types such as Plant or Trainer.
        """
    
        if obj.content_object:
            content_type = obj.content_type.model
            if content_type == 'plant':
                from biodiversity.serializers import PlantSerializer
                return PlantSerializer(obj.content_object).data
            elif content_type == 'trainer':
                from trainers.serializers import TrainerSerializer
                return TrainerSerializer(obj.content_object).data
        return None

    class Meta:
        model = NfcTag
        fields = [
            'id', 'serial_number', 'user', 'nfc_tag_type', 'active', 'label', 'content_type', 
            'object_id', 'content_object', 'created_at', 'last_modified', 'scans', 'memory'
        ]
