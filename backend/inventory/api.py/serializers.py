from rest_framework import serializers

from ..models import InventoryFormPage


class InventoryBoxSerializer(serializers.ModelSerializer):

    class Meta:
        model = InventoryFormPage
        fields = ['id', 'name', 'description', 'collection']
