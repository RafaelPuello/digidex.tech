from rest_framework import serializers

from .models import UserAssistant


class UserAssistantSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAssistant
        fields = ['user']
