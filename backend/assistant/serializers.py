from rest_framework import serializers

from .models import TrainerAssistant


class TrainerAssistantSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainerAssistant
        fields = ['trainer']
