import re

from django.core.exceptions import ValidationError


def validate_serial_number(value):
    pattern = re.compile(r'^[A-Za-z0-9]{14}$')
    if not pattern.match(value):
        raise ValidationError(
            '%(value)s is not a valid NTAG serial number',
            params={'value': value},
        )
