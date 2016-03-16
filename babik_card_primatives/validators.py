from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from babik_card_primatives.utils import check_card_number


class CardNumberValidator(object):
    """
    Uses Luhn's algorithm to validate the passed value
    """
    code = 'invalid_card_number'
    message = _('Invalid card number')

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        try:
            if not check_card_number(value):
                raise ValidationError(self.message, code=self.code)
        except ValueError:
            raise ValidationError(self.message, code=self.code)
