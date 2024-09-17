from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _

from .models import NfcTag

def link(request):
    """
    Handles the initial logic for an NFC tag link.
    """
    mirrored_values = request.GET.get('m', None)
    # Separation character "x" is automatically mirrored
    # between UID mirror and NFC counter mirror.
    if not mirrored_values or 'x' not in mirrored_values:
        messages.error(request, _('Invalid NFC tag URI.'))
        return redirect('/')

    serial_number, scan_counter = mirrored_values.split('x')
    if not serial_number:
        # MIRROR_BYTE or MIRROR_PAGE is not set properly
        messages.error(request, _('NFC Tag improperly configured.'))
        return redirect('/')

    ntag = get_object_or_404(
        NfcTag.objects.select_related('linked_object'),
        serial_number=serial_number
    )
    ntag.log_scan(request.user, scan_counter)

    if not hasattr(ntag, 'linked_object'):
        return redirect('/')
    return redirect(ntag.linked_object.url)
