from rest_framework import viewsets, permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Box
from .serializers import BoxSerializer


class BoxAPIViewSet(viewsets.ModelViewSet):
    queryset = Box.objects.all()
    base_serializer_class = BoxSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'uuid'
    body_fields = ['uuid', 'owner', 'description']
    meta_fields = ['uuid']
