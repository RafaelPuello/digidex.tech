from rest_framework import serializers

from .models import Trainer, TrainerPage


class TrainerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Trainer
        fields = ['url', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined']


class TrainerPageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TrainerPage
        fields = ['url', 'trainer', 'bio', 'location', 'birth_date']
