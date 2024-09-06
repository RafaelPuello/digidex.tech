from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.http import Http404
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.images.api.v2.views import ImagesAPIViewSet

from .models import UserInventory, Entity, EntityGalleryImage
from .serializers import UserInventorySerializer, InventoryEntitySerializer, EntityGalleryImageSerializer


class UserInventoryAPIViewSet(PagesAPIViewSet):
    model = UserInventory
    base_serializer_class = UserInventorySerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'uuid'
    body_fields = ['uuid', 'slug', 'title', 'description', 'body', 'url', 'entities']
    meta_fields = ['uuid']


class InventoryEntityAPIViewSet(PagesAPIViewSet):
    models = Entity
    base_serializer_class = InventoryEntitySerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'uuid'
    body_fields = ['uuid', 'slug', 'title', 'description', 'body', 'url', 'image']
    meta_fields = ['uuid']


class EntityGalleryImageAPIViewSet(ImagesAPIViewSet):
    models = EntityGalleryImage
    base_serializer_class = EntityGalleryImageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'uuid'
    body_fields = ['uuid', 'slug', 'title', 'description', 'body', 'url', 'entities']
    meta_fields = ['uuid']
