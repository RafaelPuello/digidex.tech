from rest_framework import serializers
from wagtail.images.api.fields import ImageRenditionField

from .models import UserPlant, UserPlantGalleryImage


class UserPlantGalleryImageSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserPlantGalleryImage model.
    """
    thumbnail = ImageRenditionField('fill-100x100', source='image')
    featured = ImageRenditionField('fill-300x300', source='image')
    detail = ImageRenditionField('max-800x800', source='image')

    class Meta:
        model = UserPlantGalleryImage
        fields = [
            'id', 'image',
            'caption', 'sort_order'
            'thumbnail', 'featured', 'detail'
        ]


class UserPlantSerializer(serializers.ModelSerializer):
    """
    Main serializer for the UserPlant model.
    """
    gallery_images = UserPlantGalleryImageSerializer(many=True, read_only=True)

    class Meta:
        model = UserPlant
        fields = ['id', 'user', 'name', 'description', 'gallery_images']