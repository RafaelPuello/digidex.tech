import uuid
from rest_framework import serializers
from wagtail.images.api.fields import ImageRenditionField

from .models import Plant, PlantGalleryImage


class PlantGalleryImageSerializer(serializers.ModelSerializer):
    """
    Serializer for the PlantGalleryImage model.
    """
    thumbnail = ImageRenditionField('fill-100x100', source='image')
    featured = ImageRenditionField('fill-300x300', source='image')
    detail = ImageRenditionField('max-800x800', source='image')

    class Meta:
        model = PlantGalleryImage
        fields = [
            'id', 'image',
            'caption', 'sort_order'
            'thumbnail', 'featured', 'detail'
        ]


class PlantSerializer(serializers.ModelSerializer):
    """
    Main serializer for the Plant model.
    """
    gallery_images = PlantGalleryImageSerializer(many=True, read_only=True)

    class Meta:
        model = Plant
        fields = ['id', 'box', 'name', 'description', 'gallery_images']