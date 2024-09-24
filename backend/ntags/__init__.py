from django.conf import settings

NTAG213 = "213"
NTAG215 = "215"
NTAG216 = "216"

NTAG_FILTER_METHODS = [
    'uid',
    'counter',
    'uid_counter'
]

NTAG_IC_CHOICES = (
    (NTAG213, "NTAG 213"),
    (NTAG215, "NTAG 215"),
    (NTAG216, "NTAG 216"),
)

NTAG_EEPROM_SIZES = {
    NTAG213: 180,
    NTAG215: 540,
    NTAG216: 924,
}


def get_nfc_tag_model_string():
    """
    Returns the dotted app.Model name for the NFCTag model as a string.
    """
    return getattr(settings, 'NFC_TAG_MODEL', 'ntags.NFCTag')


def get_nfc_tag_model():
    """
    Returns the NFCTag model that is active in this project.
    """
    from django.apps import apps

    model_string = get_nfc_tag_model_string()
    try:
        return apps.get_model(model_string, require_ready=False)
    except ValueError:
        raise ValueError('NFC_TAG_MODEL must be of the form "app_label.model_name"')
    except LookupError:
        raise ValueError('NFC_TAG_MODEL refers to model "{}" that has not been installed'.format(model_string))


def get_nfc_tag_filter_method():
    """
    Returns the method to filter NFC tags that is active in this project.
    """

    filter_method =  getattr(settings, 'NFC_TAG_FILTER_METHOD', 'uid')
    if filter_method not in NTAG_FILTER_METHODS:
        raise ValueError('Invalid filter method for NFC tags. Valid options are: {}'.format(NTAG_FILTER_METHODS))
    return filter_method
