from rest_framework import serializers

from .models import NFCTagDesign, NFCTag, NFCTagScan, NFCTagMemory


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


class NFCTagMemorySerializer(serializers.ModelSerializer):
    """
    Serializer for the NFCTagMemory model, representing the memory contents of an NFC tag.
    Includes details about the memory content, the integrated circuit type, and timestamps.
    """

    class Meta:
        model = NFCTagMemory
        fields = ['uuid', 'ntag', 'integrated_circuit', 'memory', 'created_at', 'last_modified']


class NFCTagSerializer(serializers.ModelSerializer):
    """
    Main serializer for the NFCTag model. It includes related scans and memory contents,
    as well as information about the associated content object through the GenericForeignKey.
    """

    content_object = serializers.SerializerMethodField()
    scans = NFCTagScanSerializer(many=True, read_only=True)
    memory = NFCTagMemorySerializer(read_only=True)

    def get_content_object(self, obj):
        """
        Dynamically retrieves the object represented by the GenericForeignKey. This function can
        be extended to handle various content types such as Plant or User.
        """

        if obj.content_object:
            content_type = obj.content_type.model
            if content_type == 'plant':
                from biology.serializers import PlantSerializer
                return PlantSerializer(obj.content_object).data
            elif content_type == 'user':
                from accounts.serializers import UserSerializer
                return UserSerializer(obj.content_object).data
        return None

    class Meta:
        model = NFCTag
        fields = [
            'id', 'serial_number', 'user', 'design', 'active', 'label', 'content_type',
            'object_id', 'content_object', 'created_at', 'last_modified', 'scans', 'memory'
        ]
