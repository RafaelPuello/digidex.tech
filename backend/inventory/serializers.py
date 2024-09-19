from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from .models import Box, BoxItem


class BoxItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the BoxItem model. It handles items stored in a box, which can be of various
    types. The content_type and object_id fields are used to represent a GenericForeignKey, and
    content_object is dynamically serialized depending on the object type (currently limited to Plant).
    """

    content_type = serializers.SlugRelatedField(
        slug_field='model',
        queryset=ContentType.objects.all(),
        required=False
    )
    content_object = serializers.SerializerMethodField()

    def get_content_object(self, obj):
        """
        Dynamically retrieves the object represented by the GenericForeignKey. In this case,
        it serializes the object if it is a Plant. The logic can be extended to handle other types.
        """
        from biology.models import Plant
        from biology.serializers import PlantSerializer
        if isinstance(obj.content_object, Plant):
            return PlantSerializer(obj.content_object).data
        return None

    class Meta:
        model = BoxItem
        fields = ['id', 'content_type', 'object_id', 'content_object', 'created_at', 'last_modified']


class BoxSerializer(serializers.ModelSerializer):
    """
    Main serializer for the Box model. This serializer includes nested serializers for
    related items (BoxItem), providing a complete representation of a box with its associated data.
    """

    items = BoxItemSerializer(many=True)

    class Meta:
        model = Box
        fields = ['id', 'owner', 'name', 'description', 'slug', 'uuid', 'collection', 'items']
