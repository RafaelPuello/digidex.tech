from rest_framework import serializers
from wagtail.images.api.fields import ImageRenditionField
from wagtail.documents.api.v2.serializers import DocumentDownloadUrlField

from .models import Plant, PlantImage, PlantDocument


class PlantImageSerializer(serializers.ModelSerializer):
    """
    Serializer for the PlantImage model. Handles the serialization of images associated
    with a plant, using Wagtail's ImageRenditionField to provide specific image renditions.
    """

    image = ImageRenditionField('fill-800x800')

    class Meta:
        model = PlantImage
        fields = ['id', 'image', 'caption', 'sort_order']


class PlantDocumentSerializer(serializers.ModelSerializer):
    """
    Serializer for the PlantDocument model. Handles the serialization of documents 
    associated with a plant, providing a download URL for the document using 
    Wagtail's DocumentDownloadUrlField.
    """

    document = DocumentDownloadUrlField()

    class Meta:
        model = PlantDocument
        fields = ['id', 'document', 'caption', 'sort_order']


class PlantSerializer(serializers.ModelSerializer):
    """
    Main serializer for the Plant model. It includes nested serializers for images 
    (PlantImageSerializer) and documents (PlantDocumentSerializer), allowing a complete 
    representation of a plant along with its associated images and documents.
    """

    images = PlantImageSerializer(many=True)
    documents = PlantDocumentSerializer(many=True)

    class Meta:
        model = Plant
        fields = ['id', 'name', 'description', 'images', 'documents']
