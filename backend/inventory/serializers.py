from rest_framework import serializers

from .models import InventoryBox


class InventoryBoxSerializer(serializers.ModelSerializer):

    class Meta:
        model = InventoryBox
        fields = ['uuid', 'owner', 'description']
