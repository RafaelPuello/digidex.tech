from rest_framework import serializers

from .models import Box, BoxItem


class BoxItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the BoxItem model. It handles items stored in a box, which can be of various
    types. The content field is a JSONField that can store any type of data.
    """
    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        """
        Dynamically retrieves the object represented by the content field (JSONField).
        """
        pass

    class Meta:
        model = BoxItem
        fields = ['id', 'content', 'created_at', 'last_modified']


class BoxSerializer(serializers.ModelSerializer):
    """
    Main serializer for the Box model. This serializer includes nested serializers for
    related items (BoxItem), providing a complete representation of a box with its associated data.
    """
    items = BoxItemSerializer(many=True)

    class Meta:
        model = Box
        fields = ['id', 'owner', 'name', 'description', 'slug', 'uuid', 'collection', 'items']
