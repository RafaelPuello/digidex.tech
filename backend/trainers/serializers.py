from rest_framework import serializers

from .models import Trainer


class TrainerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Trainer
        fields = ['url', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined']
