from rest_framework import viewsets, permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import TrainerInventory
from .serializers import TrainerInventorySerializer


class TrainerInventoryAPIViewSet(viewsets.ModelViewSet):
    queryset = TrainerInventory.objects.all()
    base_serializer_class = TrainerInventorySerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'uuid'
    body_fields = ['uuid', 'trainer', 'description']
    meta_fields = ['uuid']
