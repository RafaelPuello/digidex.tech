from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import UserPlant
from .serializers import UserPlantSerializer


class UserPlantViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing UserPlant instances.
    """
    queryset = UserPlant.objects.all()
    serializer_class = UserPlantSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return UserPlant.objects.filter(user=self.request.user)
