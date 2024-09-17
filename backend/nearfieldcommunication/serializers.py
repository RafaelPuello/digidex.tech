from rest_framework import serializers

from .models import NfcTag, NfcTagType, NfcTagScan, NfcTagMemory


class NfcTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = NfcTag
        fields = ['serial_number', 'user', 'nfc_tag_type', 'active']

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
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance


class NfcTagTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = NfcTagType
        fields = ['name', 'description']

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


class NfcTagMemorySerializer(serializers.ModelSerializer):

    class Meta:
        model = NfcTagMemory
        fields = ['uuid', 'nfc_tag', 'integrated_circuit', 'memory']

    def create(self, validated_data):
        """
        Create and return a new `NfcTagMemory` instance, given the validated data.
        """
        return NfcTagMemory.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `NfcTagMemory` instance, given the validated data.
        """
        instance.integrated_circuit = validated_data.get('integrated_circuit', instance.integrated_circuit)
        instance.memory = validated_data.get('memory', instance.memory)
        instance.save()
        return instance
