from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _

from .models import UserAssistant


@login_required()
def chat(request):
    """
    Chat with the requested user's chat bot assistant.
    """

    question = request.GET.get('question')
    if not question:
        return JsonResponse({'error': _('Missing question parameter.')}, status=400)
    assistant = UserAssistant.objects.get(user=request.user)
    chat = assistant.chat(question)
    return JsonResponse({'chat': chat})
