from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

#### Example

# def validate_even(value):
#     if value % 2 != 0:
#         raise ValidationError(
#             _('%(value)s is not an even number'),
#             params={'value': value},
#         )


def validate_not_null(value):
    if value is None:
        raise ValidationError(
            _('%(value)s is null.'),
            params={'value': value},
        )