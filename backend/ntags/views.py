from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from .models import NFCTag


def link_nfc_tag(request):
    """
    Link an NTAG using the ASCII Mirror embedded in the NTAG's URL.
    """
    mirrored_values = request.GET.get('m', None)

    if not mirrored_values or 'x' not in mirrored_values:
        messages.error(request, _('Invalid mirror values.'))
        return redirect('/')

    uid, counter = mirrored_values.split('x')

    try:
        nfc_tag = NFCTag.objects.get(serial_number=uid)

        if not request.user.is_authenticated:
            nfc_tag.log_scan(counter)
            return redirect(nfc_tag.url)

        else:
            nfc_tag.log_scan(counter, request.user)

            if request.user != nfc_tag.user:
                return redirect(nfc_tag.url)

            return render(
                request,
                'nfctags/index.html',
                {'urls': nfc_tag.get_urls()}
            )

    except NFCTag.objects.model.DoesNotExist:
        messages.error(request, _('NFC Tag not found.'))
        return redirect('/')


def get_linkable_objects(request, objects_id):
    """
    Get the objects that can be linked to an NTAG.
    """
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
