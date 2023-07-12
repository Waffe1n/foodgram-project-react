import re

from django.core.exceptions import ValidationError


def color_validation(value):
    """Check whether username corresponds to the requirements."""
    if not re.match('^#([A-Fa-f0-9]{6})$', value):
        raise ValidationError(
            'Hex color should consist of 6 "1-9" digist',
            ' or "a(A)-f(F)" letters.')
    return value
