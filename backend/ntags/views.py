from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render, get_object_or_404
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
    nfc_tag = NFCTag.object.get(uid=uid)
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


@login_required
def register_nfc_tag(request, uid):
    """
    Register an NFC Tag with the given UID and link it to the current user.
    """
    nfc_tag = get_object_or_404(NFCTag, uid=uid)

    # Set the user field to the current user if not already set
    if nfc_tag.user is None:
        nfc_tag.user = request.user
        nfc_tag.save()
        messages.success(request, _('NFC Tag successfully registered to your account.'))
    else:
        messages.info(request, _('This NFC Tag is already registered.'))

    return redirect(get_nfc_tag_fallback_url())
