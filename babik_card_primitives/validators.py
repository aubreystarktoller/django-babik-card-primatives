import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from babik_card_primitives.utils import (
    card_number_luhn_test,
    get_card_issuer
)


class CardNumberLuhnTestValidator(object):
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
            if not card_number_luhn_test(value):
                raise ValidationError(self.message, code=self.code)
        except ValueError:
            raise ValidationError(self.message, code=self.code)


class CardNumberIssuerWhiteListValidator(object):
    code = 'invalid_issuer'
    message = _('Invalid issuer')

    def __init__(self, whitelist, message=None, code=None):
        self.whitelist = whitelist
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        issuer = get_card_issuer(value)
        if issuer not in self.whitelist:
            raise ValidationError(self.message, code=self.code)


class CardSecurityCodeValidator(object):
    code = 'invalid_csc'
    message = _('Invalid card security code')
    regex = re.compile('^[0-9]{3,4}$')

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        if not self.regex.match(value):
            raise ValidationError(self.message, code=self.code)
