from rest_framework import serializers

from .models import InventoryBoxPage


class InventoryBoxSerializer(serializers.ModelSerializer):

    class Meta:
        model = InventoryBoxPage
        fields = ['id', 'name', 'description', 'collection']
