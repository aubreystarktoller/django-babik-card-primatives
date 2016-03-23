import logging

from django.conf import settings
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from django import forms
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text

from babik_card_primitives.exceptions import InvalidCardNumber
from babik_card_primitives.two_field_date import TwoFieldDate
from babik_card_primitives.utils import clean_card_number
from babik_card_primitives.validators import (
    CardNumberLuhnTestValidator,
    CardNumberIssuerWhitelistValidator,
    CardSecurityCodeValidator
)
from babik_card_primitives.widgets import (
    SensitiveInput,
    SensitiveSelect,
    TwoFieldDateWidget
)


CARD_NUMBER_MIN_LENGTH = 10
CARD_NUMBER_MAX_LENGTH = 25
DEFAULT_TWO_FIELD_INPUT_FORMATS = ["%m%Y"]


class CardNumberField(forms.Field):
    widget = SensitiveInput

    default_error_messages = {
        'invalid': _('Invalid card number'),
        'invalid_issuer': _('Invalid issuer'),
    }

    def __init__(self, use_luhn_test=True, client_side_only=False,
                 issuer_whitelist=None, *args, **kwargs):
        self.client_side_only = client_side_only
        if client_side_only:
            kwargs['required'] = False

        super(CardNumberField, self).__init__(*args, **kwargs)

        self.validators.append(MinLengthValidator(CARD_NUMBER_MIN_LENGTH))
        self.validators.append(MaxLengthValidator(CARD_NUMBER_MAX_LENGTH))
        if use_luhn_test:
            self.validators.append(
                CardNumberLuhnTestValidator(
                    self.error_messages['invalid'],
                    code='invalid'
                )
            )
        if issuer_whitelist:
            self.validators.append(
                CardNumberIssuerWhitelistValidator(
                    issuer_whitelist,
                    self.error_messages['invalid_issuer'],
                    code='invalid_issuer'
                )
            )

    def to_python(self, value):
        if self.client_side_only and value not in self.empty_values:
            logger = logging.getLogger('babik_card_primatives')
            logger.critical(
                "Data that should not have reached the server has"
                " reached the server."
            )
            return None
        elif value in self.empty_values:
            return ''
        else:
            value = force_text(value)
            try:
                return clean_card_number(value)
            except InvalidCardNumber:
                raise ValidationError(
                    self.error_messages['invalid'],
                    code='invalid'
                )

    def widget_attrs(self, widget):
        attrs = super(CardNumberField, self).widget_attrs(widget)
        attrs.update({
            'maxlength': str(CARD_NUMBER_MAX_LENGTH),
            'client_side_only': self.client_side_only,
        })
        return attrs


class SensitiveChoiceField(forms.ChoiceField):
    widget = SensitiveSelect

    def __init__(self, client_side_only=False, *args, **kwargs):
        self.client_side_only = client_side_only
        if client_side_only:
            kwargs['required'] = False
        super(SensitiveChoiceField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if self.client_side_only and value not in self.empty_values:
            logger = logging.getLogger('babik_card_primatives')
            logger.critical(
                "Data that should not have reached the server has"
                " reached the server."
            )
            return None
        else:
            return super(SensitiveChoiceField, self).to_python(value)

    def widget_attrs(self, widget):
        attrs = super(SensitiveChoiceField, self).widget_attrs(widget)
        if self.client_side_only:
            attrs['client_side_only'] = True
        return attrs


class CardSecurityCodeField(forms.CharField):
    widget = SensitiveInput

    default_error_messages = {
        'invalid_csc': _('Invalid card security code'),
    }

    def __init__(self, client_side_only=False, *args, **kwargs):
        kwargs['max_length'] = 4
        kwargs['min_length'] = 3
        self.client_side_only = client_side_only
        if client_side_only:
            kwargs['required'] = False
        super(CardSecurityCodeField, self).__init__(*args, **kwargs)
        self.validators.append(
            CardSecurityCodeValidator(
                self.error_messages['invalid_csc'],
                code='invalid_csc'
            )
        )

    def to_python(self, value):
        if self.client_side_only and value not in self.empty_values:
            logger = logging.getLogger('babik_card_primatives')
            logger.critical(
                "Data that should not have reached the server has"
                " reached the server."
            )
            return None
        elif value in self.empty_values:
            return ''
        else:
            value = force_text(value)
            return value.strip()

    def widget_attrs(self, widget):
        attrs = super(CardSecurityCodeField, self).widget_attrs(widget)
        if self.client_side_only:
            attrs['client_side_only'] = True
        return attrs


class TwoFieldDateField(forms.Field):
    widget = TwoFieldDateWidget

    default_error_messages = {
        'invalid': _('Invalid date'),
        'invalid_month': _('Invalid date (month is invalid)'),
        'invalid_year': _('Invalid date (year is invalid)'),
    }

    def __init__(self, input_formats=None, client_side_only=False, *args,
                 **kwargs):
        self.client_side_only = client_side_only

        self._input_formats = input_formats

        if client_side_only:
            kwargs['required'] = False
        super(TwoFieldDateField, self).__init__(*args, **kwargs)

    @property
    def input_formats(self):
        if self._input_formats:
            return self._input_formats
        else:
            return getattr(
                settings,
                'TWO_FIELD_INPUT_FORMATS',
                DEFAULT_TWO_FIELD_INPUT_FORMATS
            )

    @input_formats.setter
    def input_formats(self, value):
        self._input_formats = value

    def _dict_to_value(self, dict_):
        try:
            month = int(dict_['month'])
        except ValueError:
            raise ValidationError(
                self.error_messages['invalid_month'],
                code='invalid_month'
            )
        if month < 1 or month > 12:
            raise ValidationError(
                self.error_messages['invalid_month'],
                code='invalid_month'
            )

        try:
            year = int(dict_['year'])
        except ValueError:
            raise ValidationError(
                self.error_messages['invalid_year'],
                code='invalid_year'
            )

        return TwoFieldDate(year, month)

    def to_python(self, value):
        if self.client_side_only and value not in self.empty_values:
            logger = logging.getLogger('babik_card_primatives')
            logger.critical(
                "Data that should not have reached the server has"
                " reached the server."
            )
            return None
        elif value in self.empty_values:
            return None
        elif isinstance(value, TwoFieldDate):
            return value
        elif isinstance(value, dict):
            return self._dict_to_value(value)
        else:
            unicode_value = force_text(value, strings_only=True)
            if isinstance(unicode_value, six.text_type):
                value = unicode_value.strip()
                if isinstance(value, six.text_type):
                    for format in self.input_formats:
                        try:
                            return TwoFieldDate.parse(value, format)
                        except (ValueError, TypeError):
                            continue
            raise ValidationError(
                self.error_messages['invalid'],
                code='invalid'
            )

    def widget_attrs(self, widget):
        attrs = super(TwoFieldDateField, self).widget_attrs(widget)
        if self.client_side_only:
            attrs['client_side_only'] = True
        return attrs
