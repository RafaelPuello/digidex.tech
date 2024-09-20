import re
from django.core.exceptions import ValidationError

from .constants import IC_CHOICES


def validate_serial_number(value):
    """
    Validates the NTAG serial number format.
    """
    pattern = re.compile(r'^[A-Za-z0-9]{14}$')
    if not pattern.match(value):
        raise ValidationError(
            '%(value)s is not a valid NTAG serial number',
            params={'value': value},
        )

def validate_integrated_circuit(value):
    """
    Validates the NTAG integrated circuit type.
    """
    if value not in dict(IC_CHOICES).keys():
        raise ValidationError(
            '%(value)s is not a valid NTAG integrated circuit type',
            params={'value': value},
        )
