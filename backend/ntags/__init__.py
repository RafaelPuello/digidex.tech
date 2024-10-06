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

def get_nfc_tag_filter_method():
    """
    Returns the method to filter NFC tags that is active in this project.
    """
    filter_method =  getattr(settings, 'NFC_TAG_FILTER_METHOD', 'uid')
    if filter_method not in NTAG_FILTER_METHODS:
        raise ValueError('Invalid filter method for NFC tags. Valid options are: {}'.format(NTAG_FILTER_METHODS))
    return filter_method

def get_nfc_taggable_model_strings():
    """
    Returns a list of model strings that are taggable by NFC tags.
    """
    return getattr(settings, 'NFC_TAGGABLE_MODELS', [])

def get_nfc_taggable_models():
    """
    Returns a list of models that are taggable by NFC tags.
    """
    from django.db.models import Q as query

    taggable_models = get_nfc_taggable_model_strings()

    conditions = [
        query(app_label=app_label, model=model_name.lower()) for app_label, model_name in (model.split('.') for model in taggable_models)
        ]

    return query() if not conditions else conditions[0] if len(conditions) == 1 else query(*conditions, _connector=query.OR)
