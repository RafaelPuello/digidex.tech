from rest_framework import viewsets, permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import InventoryBox
from .serializers import InventoryBoxSerializer


class InventoryBoxAPIViewSet(viewsets.ModelViewSet):
    queryset = InventoryBox.objects.all()
    base_serializer_class = InventoryBoxSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'uuid'
    body_fields = ['uuid', 'owner', 'description']
    meta_fields = ['uuid']
