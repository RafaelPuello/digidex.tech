from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from .utils import get_nfc_tag_model


def link(request):
    """
    Handles the initial logic for an NFC tag link.
    """

    mirrored_values = request.GET.get('m', None)

    if not mirrored_values:
        messages.error(request, _('Invalid NFC tag URI.'))
        return redirect('/')

    NFCTag = get_nfc_tag_model()

    try:
        ntag = NFCTag.objects.get_from_mirror(mirrored_values)
        return redirect(ntag.get_absolute_url())

    except ValueError as e:
        messages.error(request, str(e))
        return redirect('/')

    except NFCTag.DoesNotExist as e:
        messages.error(request, str(e))
        return redirect('/')
