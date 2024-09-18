from rest_framework import serializers
from wagtail.images.api.fields import ImageRenditionField
from wagtail.documents.api.v2.serializers import DocumentDownloadUrlField
from django.contrib.contenttypes.models import ContentType

from biodiversity.models import Plant
from .models import Box, BoxImage, BoxDocument, BoxItem


class BoxImageSerializer(serializers.ModelSerializer):
    """
    Serializer for the BoxImage model. It handles the serialization of the images
    related to a box, using Wagtail's ImageRenditionField to get a specific rendition
    of the image.
    """

    image = ImageRenditionField('fill-800x800')

    class Meta:
        model = BoxImage
        fields = ['id', 'image', 'caption', 'sort_order']


class BoxDocumentSerializer(serializers.ModelSerializer):
    """
    Serializer for the BoxDocument model. It handles the serialization of documents 
    associated with a box, using Wagtail's DocumentDownloadUrlField to provide the download 
    URL for the document.
    """

    document = DocumentDownloadUrlField()

    class Meta:
        model = BoxDocument
        fields = ['id', 'document', 'caption', 'sort_order']


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

        if isinstance(obj.content_object, Plant):
            from biodiversity.serializers import PlantSerializer
            return PlantSerializer(obj.content_object).data
        return None

    class Meta:
        model = BoxItem
        fields = ['id', 'content_type', 'object_id', 'content_object', 'created_at', 'last_modified']


class BoxSerializer(serializers.ModelSerializer):
    """
    Main serializer for the Box model. This serializer includes nested serializers for
    related images (BoxImage), documents (BoxDocument), and items (BoxItem), providing
    a complete representation of a box with its associated data.
    """

    images = BoxImageSerializer(many=True)
    documents = BoxDocumentSerializer(many=True)
    items = BoxItemSerializer(many=True)

    class Meta:
        model = Box
        fields = ['id', 'owner', 'name', 'description', 'slug', 'uuid', 'images', 'documents', 'items']
