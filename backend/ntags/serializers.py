from rest_framework import serializers

from .models import NFCTagDesign, NFCTag, NFCTagScan, NFCTagEEPROM


class NFCTagDesignSerializer(serializers.ModelSerializer):
    """
    Serializer for the NFCTagDesign model.
    """

    class Meta:
        model = NFCTagDesign
        fields = ['id', 'name', 'description', 'designer', 'uuid', 'collection']


class NFCTagScanSerializer(serializers.ModelSerializer):
    """
    Serializer for the NFCTagScan model, representing scans of an NFC tag.
    """

    scanned_by = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = NFCTagScan
        fields = ['id', 'ntag', 'counter', 'scanned_by', 'scanned_at']


class NFCTagEEPROMSerializer(serializers.ModelSerializer):
    """
    Serializer for the NFCTagEEPROM model, representing the eeprom contents of an NFC tag.
    """

    class Meta:
        model = NFCTagEEPROM
        fields = ['uuid', 'ntag', 'eeprom', 'created_at', 'last_modified']


class NFCTagSerializer(serializers.ModelSerializer):
    """
    Main serializer for the NFCTag model.
    """

    scans = NFCTagScanSerializer(
        many=True,
        read_only=True
    )
    eeprom = NFCTagEEPROMSerializer(
        read_only=True
    )

    def get_content_object(self, obj):
        pass

    class Meta:
        model = NFCTag
        fields = [
            'id', 'serial_number', 'integrated_circuit', 'design', 'active', 'user',
            'created_at', 'last_modified', 'scans', 'eeprom'
        ]
