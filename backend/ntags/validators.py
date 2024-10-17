import re
from django.core.exceptions import ValidationError


def validate_ascii_mirror(value):
    """
    Validate the ASCII Mirror-Based UID and counter format.
    Based on NXP Semiconductors documentation.
    """
    if 'x' not in value:
        raise ValidationError(
            '%(value)s is not a valid mirror value (missing separator).',
            params={'value': value},
        )

    # Split and call the separate validators for UID and Counter
    uid, counter = value.split('x', 1)
    validate_ascii_mirror_uid(uid)
    validate_ascii_mirror_counter(counter)
    return uid, counter


def validate_ascii_mirror_counter(value):
    """
    Validate the ASCII Mirror-Based counter format.
    The counter should be a 3-byte hex value in ASCII representation.
    Each byte should be represented by 2 characters so the total length should be 6 characters.
    """
    pattern = re.compile(r'^[0-9A-Fa-f]{6}$')
    if not pattern.match(value):
        raise ValidationError(
            '%(value)s is not a valid counter value.',
            params={'value': value},
        )


def validate_ascii_mirror_uid(value):
    """
    Validates the ASCII Mirror-Based NTAG uid format.
    The uid should be a 7-byte hex value in ASCII representation.
    Each byte should be represented by 2 characters so the total length should be 14 characters.
    """
    pattern = re.compile(r'^[0-9A-Fa-f]{14}$')
    if not pattern.match(value):
        raise ValidationError(
            '%(value)s is not a valid UID (Serial Number).',
            params={'value': value},
        )
