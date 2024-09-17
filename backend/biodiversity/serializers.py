from rest_framework import serializers

from biodiversity.models import Plant


class PlantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plant
        fields = ['name', 'description']
