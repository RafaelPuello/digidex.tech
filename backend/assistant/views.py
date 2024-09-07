from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _

from .models import TrainerAssistant

@login_required()
def chat(request):
    question = request.GET.get('question')
    if not question:
        return JsonResponse({'error': _('Missing question parameter.')}, status=400)
    assistant = TrainerAssistant.objects.get(user=request.user)
    chat = assistant.chat(question)
    return JsonResponse({'chat': chat})
