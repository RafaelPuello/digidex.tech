from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from .models import NFCTag


def link_nfc_tag(request):
    """
    Link an NTAG using the ASCII Mirror embedded in the NTAG's URL.
    """
    mirrored_values = request.GET.get('m', None)
    if not mirrored_values:
        messages.error(request, _('Invalid mirror values.'))
        return redirect('/')

    try:
        ntag = NFCTag.objects.get_from_mirror(mirrored_values)
        return redirect(ntag.url)
    except Exception as e:
        messages.error(request, str(e))
        return redirect('/')


def get_linkable_objects(request, objects_id):
    try:
        content_type = ContentType.objects.get(id=objects_id)
        model_class = content_type.model_class()
        objects = model_class.objects.all()

        data = {
            'objects': [{'id': obj.id, 'name': str(obj)} for obj in objects]
        }

        return JsonResponse(data)

    except ContentType.DoesNotExist:
        return JsonResponse({'error': 'Invalid content type'}, status=400)
