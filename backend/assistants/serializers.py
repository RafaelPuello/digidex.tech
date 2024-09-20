from rest_framework import serializers

from .models import UserAssistant


class UserAssistantSerializer(serializers.ModelSerializer):
    """
    A serializer for the UserAssistant model.
    """
    class Meta:
        model = UserAssistant
        fields = ['user']
