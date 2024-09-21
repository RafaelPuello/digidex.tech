from rest_framework import serializers

from .models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    A serializer for the User model.
    """

    class Meta:
        model = User
        fields = ['uuid', 'username', 'first_name', 'last_name', 'email', 'groups', 'user_permissions', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined']
