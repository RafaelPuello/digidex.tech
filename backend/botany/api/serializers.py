from rest_framework import serializers
from wagtail.images.api.fields import ImageRenditionField

from ..models import UserPlant


class UserPlantSerializer(serializers.ModelSerializer):
    """
    Main serializer for the UserPlant model.
    """
    thumbnail = ImageRenditionField('fill-100x100', source='image')
    featured = ImageRenditionField('fill-300x300', source='image')
    detail = ImageRenditionField('max-800x800', source='image')

    class Meta:
        model = UserPlant
        fields = ['id', 'box', 'name', 'description', 'thumbnail', 'featured', 'detail', 'taxon_id', 'substrate', 'notes', 'active']
