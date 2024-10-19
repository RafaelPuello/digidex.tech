import warnings


def get_inventory_model_strings():
    """
    Returns a list of model strings that are part of the inventory..
    """
    from django.conf import settings

    inventory_models = getattr(settings, 'INVENTORY_MODELS', None)
    if inventory_models is None:
        warnings.warn(
            "INVENTORY_MODELS is not set. Defaulting to an empty list.",
            UserWarning
        )
        return []
    return inventory_models

def get_inventory_models():
    """
    Returns a query combining all models that are part of the inventory.
    """
    from django.db.models import Q as query

    # Return an empty Q object if there are no inventory models
    inventory_models = get_inventory_model_strings()
    if not inventory_models:
        return query()

    # Build conditions using the inventory models
    conditions = [
        query(app_label=app_label, model=model_name.lower()) for app_label, model_name in (model.split('.') for model in inventory_models)
    ]

    # Combine all conditions with OR
    return conditions[0] if len(conditions) == 1 else query(*conditions, _connector=query.OR)
