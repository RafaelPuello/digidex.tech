from rest_framework import viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Box, BoxItem
from .serializers import BoxSerializer, BoxItemSerializer


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
    body_fields = ['id', 'owner', 'name', 'description', 'slug', 'uuid', 'items']
    meta_fields = ['id']

    def get_queryset(self):
        """
        Filter to only show boxes associated with each user.
        """
        return Box.objects.filter(user=self.request.user)
