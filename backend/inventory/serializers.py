from rest_framework import serializers

from .models import TrainerInventory


class TrainerInventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = TrainerInventory
        fields = ['uuid', 'trainer', 'description']
