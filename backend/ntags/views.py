from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from . import get_nfc_tag_model

def link(request):
    """
    Handles the initial logic for an NFC tag link.
    """
    mirrored_values = request.GET.get('m', None)
    if not mirrored_values:
        messages.error(request, _('Invalid mirror values.'))
        return redirect('/')

    NFCTag = get_nfc_tag_model()
    try:
        ntag = NFCTag.objects.get_from_mirror(mirrored_values)
        return redirect(ntag.linked_item.url)

    except Exception as e:
        messages.error(request, str(e))
        return redirect('/')
