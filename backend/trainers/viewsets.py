from rest_framework import permissions, viewsets

from .models import Trainer
from .serializers import TrainerSerializer


class TrainerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows trainers to be viewed or edited.
    """
    queryset = Trainer.objects.all().order_by('-date_joined')
    serializer_class = TrainerSerializer
    permission_classes = [permissions.IsAuthenticated]
