from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from . import get_nfc_tag_model, get_nfc_tag_fallback_url
from .validators import validate_ascii_mirror

NFCTag = get_nfc_tag_model()


def link_nfc_tag(request):
    """
    Link an NTAG using the ASCII Mirror embedded in the NTAG's URL.
    """
    # Check mirrored_values is in the request
    mirrored_values = request.GET.get('m', None)
    if not mirrored_values:
        messages.error(request, _('No ASCII Mirror value found.'))
        return redirect(get_nfc_tag_fallback_url())

    # Check mirrored_values is in the expected format
    try:
        uid, counter = validate_ascii_mirror(mirrored_values)
    except ValidationError as e:
        messages.error(request, _(f'Invalid ASCII Mirror value: {e}'))
        return redirect(get_nfc_tag_fallback_url())

    # Check that the NFC Tag exists
    nfc_tag = NFCTag.get_from_uid(uid)
    if not nfc_tag:
        messages.error(request, _('Invalid serial number. NFC Tag ASCII mirror improperly configured.'))
        return redirect(get_nfc_tag_fallback_url())

    scan = {'counter': counter}
    if request.user.is_authenticated:
        scan.update({'user': request.user})

    context = nfc_tag.build_context(request)

    # Attempt to log the scan and return the response
    try:
        nfc_tag.log_scan(**scan)
        messages.info(request, _(f'Logged scan #{counter} for NFC Tag'))
    except Exception as e:
        messages.error(request, _(f'Error logging scan #{counter} for NFC Tag: {e}'))
    return render(request, 'nfctags/index.html', context)


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
