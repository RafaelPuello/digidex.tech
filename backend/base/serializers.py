from rest_framework.fields import Field
from rest_framework import serializers
from wagtail.images.api.v2.serializers import BaseSerializer, ImageDownloadUrlField, ImageSerializer
from wagtail.images.api.fields import ImageRenditionField

from base.models import BaseImage


class MainImageField(Field):
    """
    Serializes the "main" field for images.

    Example:
    "main": "/media/images/a_test_image.jpg"
    """

    def get_attribute(self, instance):
        return instance

    def to_representation(self, image):
        return image.get_rendition('max-1024x882').url


class FeaturedImageField(Field):
    """
    Serializes the "featured" field for images.

    Example:
    "featured": "/media/images/a_test_image.jpg"
    """

    def get_attribute(self, instance):
        return instance

    def to_representation(self, image):
        return image.get_rendition('max-600x600').url


class ThumbnailImageField(Field):
    """
    Serializes the "thumbnail" field for images.

    Example:
    "thumbnail": "/media/images/a_test_image.jpg"
    """

    def get_attribute(self, instance):
        return instance

    def to_representation(self, image):
        return image.get_rendition('max-300x300').url


