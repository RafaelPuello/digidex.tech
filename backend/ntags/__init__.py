import warnings


def get_nfc_tag_fallback_url():
    """
    Returns the fallback URL for NFC tags.
    """
    from django.conf import settings

    fallback_url = getattr(settings, 'NFC_TAG_FALLBACK_URL', None)
    if fallback_url is None:
        warnings.warn(
            "NFC_TAG_FALLBACK_URL is not set. Defaulting to '/'.",
            UserWarning
        )
        return '/'
    return fallback_url


def get_nfc_tag_model_string():
    """
    Returns the model string for the NFCTag model.
    """
    from django.conf import settings

    tag_model = getattr(settings, 'NFC_TAG_MODEL', None)
    if tag_model is None:
        warnings.warn(
            "NFC_TAG_MODEL is not set. Defaulting to 'nfc.NFCTag'.",
            UserWarning
        )
        return 'ntags.NFCTag'
    return tag_model


def get_nfc_tag_model():
    """
    Returns the model class for the NFCTag model.
    """
    from django.apps import apps

    model_string = get_nfc_tag_model_string()
    try:
        app_label, model_name = model_string.split('.')
        return apps.get_model(app_label, model_name)
    except (ValueError, LookupError):
        raise ValueError(f"Invalid NFC_TAG_MODEL '{model_string}'")


def get_nfc_taggable_model_strings():
    """
    Returns a list of model strings that are taggable by NFC tags.
    """
    from django.conf import settings

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


def get_nfc_taggable_model_classes():
    """
    Returns a list of model classes that are taggable by NFC tags.
    """
    from django.apps import apps
    from django.contrib.contenttypes.models import ContentType

    # Get the list of model strings from settings
    model_strings = get_nfc_taggable_model_strings()
    if not model_strings:
        return ContentType.objects.none()

    # Resolve model strings to model classes
    content_types = []
    for model_string in model_strings:
        try:
            app_label, model_name = model_string.split('.')
            model_class = apps.get_model(app_label, model_name)
            if model_class:
                content_type = ContentType.objects.get_for_model(model_class)
                content_types.append(content_type)
        except (ValueError, LookupError):
            warnings.warn(f"Could not find ContentType for model: {model_string}", UserWarning)

    return ContentType.objects.filter(id__in=[ct.id for ct in content_types])
