from rest_framework import serializers

from .models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    A serializer for the User model.
    """
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined']
