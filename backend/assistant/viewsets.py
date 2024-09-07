from rest_framework import status, viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.translation import gettext as _

from .models import TrainerAssistant
from .serializers import TrainerAssistantSerializer


class TrainerAssistantDetail(viewsets.ReadOnlyModelViewSet):
    queryset = TrainerAssistant.objects.all()
    serializer_class = TrainerAssistantSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return TrainerAssistant.objects.filter(trainer=self.request.user)

    @action(detail=True, methods=['get'])
    def chat(self, request):
        question = request.GET.get('question')
        if not question:
            return Response({'error': _('Missing question parameter.')}, status=status.HTTP_400_BAD_REQUEST)
        assistant = self.get_object()
        chat = assistant.chat(question)
        return Response({'chat': chat})
