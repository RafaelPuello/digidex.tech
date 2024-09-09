from rest_framework import permissions, viewsets

from .serializers import TrainerSerializer, TrainerPageSerializer


class TrainerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows trainers to be viewed or edited.
    """
    queryset = TrainerSerializer.objects.all().order_by('-date_joined')
    serializer_class = TrainerSerializer
    permission_classes = [permissions.IsAuthenticated]


class TrainerPageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows trainer pages to be viewed or edited.
    """
    queryset = TrainerPageSerializer.objects.all().order_by('name')
    serializer_class = TrainerPageSerializer
    permission_classes = [permissions.IsAuthenticated]
