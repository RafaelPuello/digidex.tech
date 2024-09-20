from rest_framework import viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Plant
from .serializers import PlantSerializer


class PlantViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing plants.
    """
    queryset = Plant.objects.all().order_by('id')
    serializer_class = PlantSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'id'
    body_fields = ['id', 'name', 'description', 'collection']
    meta_fields = ['id']

    def get_queryset(self):
        """
        Filter to only show plant images associated with each user.
        """
        return Plant.objects.filter(user=self.request.user)
