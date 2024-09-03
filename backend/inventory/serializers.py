from rest_framework import serializers
from django.templatetags.static import static

from .models import UserInventory, Entity, EntityGalleryImage


class EntityGalleryImageSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    featured = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()
    detailed =serializers.SerializerMethodField()
    alt = serializers.SerializerMethodField()

    class Meta:
        model = EntityGalleryImage
        fields = ['title', 'featured', 'thumbnail', 'detailed', 'alt', 'caption', 'sort_order']

    def get_title(self, obj):
        return obj.image.title

    def get_featured(self, obj):
        return obj.image.get_rendition('max-600x600').url

    def get_thumbnail(self, obj):
        return obj.image.get_rendition('max-300x300').url

    def get_detailed(self, obj):
        return obj.image.get_rendition('max-1024x882').url

    def get_alt(self, obj):
        return obj.image.alt if obj.image.alt else obj.image.title


class InventoryEntitySerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Entity
        fields = ['uuid', 'slug', 'date', 'title', 'description', 'body', 'url', 'image']

    def get_image(self, obj):
        image = obj.get_main_image()
        if not image:
            return {
                'title': 'Placeholder',
                'thumbnail': static("inventory/images/placeholder.svg"),
                'alt': 'Placeholder',
                'caption': '',
                'sort_order': 0
            }
           
        return EntityGalleryImageSerializer(image).data

    def get_date(self, obj):
        return obj.get_date()


class UserInventorySerializer(serializers.ModelSerializer):
    entities = serializers.SerializerMethodField()

    class Meta:
        model = UserInventory
        fields = ['uuid', 'slug', 'title', 'description', 'body', 'url', 'entities']

    def get_entities(self, obj):
        entities = obj.get_entities()
        return InventoryEntitySerializer(entities, many=True).data
