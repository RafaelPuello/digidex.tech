from rest_framework import serializers

from .models import NFCTag, NFCTagScan, NFCTagMemory


class NFCTagScanSerializer(serializers.ModelSerializer):
    """
    Serializer for the NFCTagScan model, representing scans of an NFC tag.
    """
    def create(self, validated_data):
        instance = NFCTagScan.objects.create(**validated_data)
        return instance

    class Meta:
        model = NFCTagScan
        fields = ['id', 'ntag', 'counter', 'scanned_by', 'scanned_at']


class NFCTagMemorySerializer(serializers.ModelSerializer):
    """
    Serializer for the NFCTagMemory model, representing the eeprom contents of an NFC tag.
    """
    class Meta:
        model = NFCTagMemory
        fields = ['uuid', 'ntag', 'eeprom', 'created_at', 'last_modified']


class NFCTagSerializer(serializers.ModelSerializer):
    """
    Main serializer for the NFCTag model.
    """
    scans = NFCTagScanSerializer(
        many=True,
        read_only=True
    )
    eeprom = NFCTagMemorySerializer(
        read_only=True
    )

    def get_content_object(self, obj):
        pass

    class Meta:
        model = NFCTag
        fields = [
            'serial_number', 'integrated_circuit',
            'user', 'label', 'active',
            'scans', 'eeprom'
        ]
