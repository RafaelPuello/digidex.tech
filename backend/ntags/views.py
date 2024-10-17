from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from .validators import validate_ascii_mirror
from .models import NFCTag


def link_nfc_tag(request):
    """
    Link an NTAG using the ASCII Mirror embedded in the NTAG's URL.
    """
    mirrored_values = request.GET.get('m', None)

    if not mirrored_values:
        messages.error(request, _('No ASCII Mirror value found.'))
        return redirect(NFCTag.get_fallback_url())

    try:
        uid, counter = validate_ascii_mirror(mirrored_values)
    except ValidationError as e:
        messages.error(request, _(f'Invalid ASCII Mirror value: {e}'))
        return redirect(NFCTag.get_fallback_url())

    nfc_tag = NFCTag.get_from_uid(uid)
    if not nfc_tag:
        messages.error(request, _('Invalid serial number. NFC Tag ASCII mirror improperly configured.'))
        return redirect(NFCTag.get_fallback_url())

    context = {'heading': str(nfc_tag)}
    scan = {'counter': counter}

    if request.user.is_authenticated:
        # User is authenticated so user can be included in the scan log
        scan.update({'user': request.user})

        if request.user == nfc_tag.user:
            context.update({'urls': nfc_tag.get_owner_urls()})
        else:
            context.update({'urls': nfc_tag.get_visitor_urls()})
    else:
        context.update({'urls': nfc_tag.get_anonymous_visitor_urls()})

    try:
        nfc_tag.log_scan(**scan)
        messages.info(request, _(f'Logged scan #{counter} for NFC Tag'))
    except Exception as e:
        messages.error(request, _(f'Error logging scan #{counter} for NFC Tag: {e}'))

    messages.success(request, _('NFC Tag linked successfully'))
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
