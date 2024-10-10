import warnings
from django.conf import settings


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
