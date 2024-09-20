from rest_framework import serializers

from .models import NFCTagDesign, NFCTag, NFCTagScan, NFCTagEEPROM


class NFCTagDesignSerializer(serializers.ModelSerializer):
    """
    Serializer for the NFCTagDesign model. It includes nested serializers for images and documents
    related to the ntag design.
    """

    class Meta:
        model = NFCTagDesign
        fields = ['id', 'name', 'description', 'owner', 'uuid', 'slug', 'collection']


class NFCTagScanSerializer(serializers.ModelSerializer):
    """
    Serializer for the NFCTagScan model, representing scans of an NFC tag.
    It includes information about the scan counter, the user who scanned, and the timestamp.
    """

    scanned_by = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = NFCTagScan
        fields = ['id', 'ntag', 'counter', 'scanned_by', 'scanned_at']


class NFCTagEEPROMSerializer(serializers.ModelSerializer):
    """
    Serializer for the NFCTagEEPROM model, representing the eeprom contents of an NFC tag.
    Includes details about the eeprom content, the integrated circuit type, and timestamps.
    """

    class Meta:
        model = NFCTagEEPROM
        fields = ['uuid', 'ntag', 'integrated_circuit', 'eeprom', 'created_at', 'last_modified']


class NFCTagSerializer(serializers.ModelSerializer):
    """
    Main serializer for the NFCTag model. It includes related scans and eeprom contents,
    as well as information about the associated content object through the GenericForeignKey.
    """

    scans = NFCTagScanSerializer(many=True, read_only=True)
    eeprom = NFCTagEEPROMSerializer(read_only=True)

    def get_content_object(self, obj):
        """
        Dynamically retrieves the object represented by the GenericForeignKey. This function can
        be extended to handle various content types such as Plant or User.
        """
        pass

    class Meta:
        model = NFCTag
        fields = [
            'id', 'serial_number', 'user', 'design', 'active', 'content',
            'created_at', 'last_modified', 'scans', 'eeprom'
        ]
