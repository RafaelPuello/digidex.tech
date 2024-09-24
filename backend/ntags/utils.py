from django.conf import settings

from .constants import NTAG_FILTER_METHODS


def get_nfc_tag_model():
    """
    Returns the NFCTag model that is active in this project.
    """
    return getattr(settings, 'NFC_TAG_MODEL', 'ntags.NFCTag')


def get_nfc_tag_model_string():
    """
    Returns the dotted app.Model name for the NFCTag model as a string.
    """
    return getattr(settings, 'NFC_TAG_MODEL', 'ntags.NFCTag')


def get_nfc_tag_filter_method():
    """
    Returns the method to filter NFC tags that is active in this project.
    """

    filter_method =  getattr(settings, 'NFC_TAG_FILTER_METHOD', 'uid')
    if filter_method not in NTAG_FILTER_METHODS:
        raise ValueError('Invalid filter method for NFC tags. Valid options are: {}'.format(NTAG_FILTER_METHODS))
    return filter_method
