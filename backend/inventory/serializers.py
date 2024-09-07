from rest_framework import serializers

from .models import UserInventory


class UserInventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = UserInventory
        fields = ['uuid', 'slug', 'title', 'description', 'body', 'url']
