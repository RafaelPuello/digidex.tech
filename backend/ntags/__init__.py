import warnings
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
    Returns the method to filter NFC tags that are active in this project.
    """
    filter_method =  getattr(settings, 'NFC_TAG_FILTER_METHOD', 'uid')
    if filter_method not in NTAG_FILTER_METHODS:
        warnings.warn(
            f"Invalid NFC_TAG_FILTER_METHOD '{filter_method}'. "
            f"Falling back to default 'uid'. Valid options are: {NTAG_FILTER_METHODS}",
            UserWarning
        )
        return 'uid'
    return filter_method

def get_nfc_taggable_model_strings():
    """
    Returns a list of model strings that are taggable by NFC tags.
    """
    taggable_models = getattr(settings, 'NFC_TAGGABLE_MODELS', None)
    if taggable_models is None:
        warnings.warn(
            "NFC_TAGGABLE_MODELS is not set. Defaulting to an empty list.",
            UserWarning
        )
        return []
    return taggable_models

def get_nfc_taggable_models():
    """
    Returns a query combining all models that are taggable by NFC tags.
    """
    from django.db.models import Q as query

    # Return an empty Q object if there are no taggable models
    taggable_models = get_nfc_taggable_model_strings()
    if not taggable_models:
        return query()

    # Build conditions using the taggable models
    conditions = [
        query(app_label=app_label, model=model_name.lower()) for app_label, model_name in (model.split('.') for model in taggable_models)
    ]

    # Combine all conditions with OR
    return conditions[0] if len(conditions) == 1 else query(*conditions, _connector=query.OR)
