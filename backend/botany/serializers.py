from rest_framework import serializers

from .models import Plant


class PlantSerializer(serializers.ModelSerializer):
    """
    Main serializer for the Plant model.
    """
    class Meta:
        model = Plant
        fields = ['id', 'name', 'description']
