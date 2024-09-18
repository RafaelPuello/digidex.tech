from rest_framework import viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Box, BoxImage, BoxDocument, BoxItem
from .serializers import BoxSerializer, BoxImageSerializer, BoxDocumentSerializer, BoxItemSerializer


class BoxImageViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing box images.
    """

    queryset = BoxImage.objects.all()
    base_serializer_class = BoxImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'id'
    body_fields = ['id', 'image', 'caption', 'sort_order']
    meta_fields = ['id']

    def get_queryset(self):
        """
        Filter to only show box images associated with each user.
        """
        return BoxImage.objects.filter(user=self.request.user)


class BoxDocumentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing box documents.
    """

    queryset = BoxDocument.objects.all()
    base_serializer_class = BoxDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'id'
    body_fields = ['id', 'document', 'caption', 'sort_order']
    meta_fields = ['id']

    def get_queryset(self):
        """
        Filter to only show box documents associated with each user.
        """
        return BoxDocument.objects.filter(user=self.request.user)


class BoxItemViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing box items.
    """

    queryset = BoxItem.objects.all()
    base_serializer_class = BoxItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'id'
    body_fields = ['id', 'content_type', 'object_id', 'content_object', 'created_at', 'last_modified']
    meta_fields = ['id']

    def get_queryset(self):
        """
        Filter to only show box items associated with each user.
        """
        return BoxItem.objects.filter(user=self.request.user)


class BoxViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing boxes.
    """

    queryset = Box.objects.all()
    base_serializer_class = BoxSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'id'
    body_fields = ['id', 'owner', 'name', 'description', 'slug', 'uuid', 'images', 'documents', 'items']
    meta_fields = ['id']

    def get_queryset(self):
        """
        Filter to only show boxes associated with each user.
        """
        return Box.objects.filter(user=self.request.user)
