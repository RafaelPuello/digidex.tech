from rest_framework import serializers

from .models import NfcTag, NfcTagType, NfcTagScan


class NfcTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = NfcTag
        fields = ['uuid', 'serial_number', 'nfc_tag_type', 'active', 'trainer', 'plant']

    def create(self, validated_data):
        """
        Create and return a new `NfcTag` instance, given the validated data.
        """
        return NfcTag.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `NfcTag` instance, given the validated data.
        """
        instance.nfc_tag_type = validated_data.get('nfc_tag_type', instance.nfc_tag_type)
        instance.trainer = validated_data.get('trainer', instance.trainer)
        instance.plant = validated_data.get('plant', instance.plant)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance


class NfcTagTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = NfcTagType
        fields = ['name', 'description', 'integrated_circuit']

    def create(self, validated_data):
        """
        Create and return a new `NfcTagType` instance, given the validated data.
        """
        return NfcTagType.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `NfcTagType` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.integrated_circuit = validated_data.get('integrated_circuit', instance.integrated_circuit)
        instance.save()
        return instance


class NfcTagScanSerializer(serializers.ModelSerializer):

    class Meta:
        model = NfcTagScan
        fields = ['nfc_tag', 'counter', 'scanned_by']

    def create(self, validated_data):
        """
        Create and return a new `NfcTagScan` instance, given the validated data.
        """
        return NfcTagScan.objects.create(**validated_data)
