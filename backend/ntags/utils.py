from django.apps import apps
from django.conf import settings

def get_nfc_tag_model():
    """
    Returns the NFCTag model that is active in this project.
    """
    model_string = getattr(settings, 'NFC_TAG_MODEL', 'ntags.NFCTag')
    return apps.get_model(model_string)

def get_nfc_tag_model_string():
    """
    Returns the dotted app.Model name for the NFCTag model as a string.
    """
    return getattr(settings, 'NFC_TAG_MODEL', 'ntags.NFCTag')
