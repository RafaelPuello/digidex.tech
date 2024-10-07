from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Plant
from .serializers import PlantSerializer


class PlantViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Plant instances.
    """
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Plant.objects.filter(box__owner=self.request.user)
