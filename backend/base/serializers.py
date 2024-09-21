from rest_framework.fields import Field


class MainImageField(Field):
    """
    Serializes the "main" field for images.
    """

    def get_attribute(self, instance):
        return instance

    def to_representation(self, image):
        return image.get_rendition('max-1024x882').url


class FeaturedImageField(Field):
    """
    Serializes the "featured" field for images.
    """

    def get_attribute(self, instance):
        return instance

    def to_representation(self, image):
        return image.get_rendition('max-600x600').url


class ThumbnailImageField(Field):
    """
    Serializes the "thumbnail" field for images.
    """

    def get_attribute(self, instance):
        return instance

    def to_representation(self, image):
        return image.get_rendition('max-300x300').url
