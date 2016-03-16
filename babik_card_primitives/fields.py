import calendar
import datetime
import logging

from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from django.utils import timezone

from babik_card_primitives.exceptions import InvalidCardNumber
from babik_card_primitives.utils import clean_card_number
from babik_card_primitives.validators import (
    CardNumberLuhnTestValidator,
    CardNumberIssuerWhitelistValidator,
    CardSecurityCodeValidator
)
from babik_card_primatives.widgets import SensitiveDataInput, SensitiveSelect


CARD_NUMBER_MIN_LENGTH = 10
CARD_NUMBER_MAX_LENGTH = 25


class CardNumberField(forms.Field):
    widget = SensitiveDataInput

    default_error_messages = {
        'invalid': _('Invalid card number'),
    }

    def __init__(self, use_luhn_test=True, client_side_only=False,
                 issuer_whitelist=None, *args, **kwargs):
        self.client_side_only = client_side_only

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
        if value in self.empty_values:
            return ''
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
        super(SensitiveChoiceField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if self.client_side_only:
            if value:
                logger = logging.getLogger('babik_card_primatives')
                logger.emergency(
                    "Data that should not have reached the server has"
                    " reached the server."
                )
            else:
                return None
        else:
            return super(SensitiveChoiceField, self).to_python(value)


class TwoFieldCardDateField(forms.MultiValueField):
    none_value = (0, '---')
    default_error_messages = {
        'invalid_month': _('Invalid month'),
        'invalid_year': _('Invalid year'),
    }

    def __init__(self, empty_label=None, required=True,
                 client_side_only=False, error_messages=None, *args,
                 **kwargs):
        self.client_side_only = client_side_only
        self.required = self.required

        if isinstance(empty_label, (list, tuple)):
            if not len(empty_label) == 2:
                raise ValueError(
                    'empty_label list/tuple must have 2 elements.'
                )

            self.year_none_value = (0, empty_label[0])
            self.month_none_value = (0, empty_label[1])
        else:
            if empty_label is not None:
                self.none_value = (0, empty_label)

            self.year_none_value = self.none_value
            self.month_none_value = self.none_value

        month_values = [(str(n), '%02d' % n) for n in range(1, 13)]
        year = timezone.now().year
        year_values = [(n, str(n)) for n in range(year, year+15)]

        messages = {}
        for c in reversed(self.__class__.__mro__):
            messages.update(getattr(c, 'default_error_messages', {}))
        messages.update(error_messages or {})

        fields = (
            SensitiveChoiceField(
                choices=[self.month_empty_value] + month_values,
                error_messages={'invalid': messages['invalid_month']},
                client_side_only=client_side_only,
            ),
            SensitiveChoiceField(
                choices=[self.year_empty_value] + year_values,
                error_messages={'invalid': messages['invalid_year']},
                client_side_only=client_side_only,
            )
        )
        return super(TwoFieldCardDateField, self).__init__(
            fields,
            require_all_fields=required,
            *args,
            **kwargs
        )

    def compress(self, data_list):
        if data_list:
            month = int(data_list[0])
            year = int(data_list[1])
            day = calendar.monthrange(year, month)[1]
            return datetime.date(year, month, day)
        else:
            return None


class CardSecurityCodeField(forms.CharField):
    widget = SensitiveDataInput

    default_error_messages = {
        'invalid': _('Invalid card security code'),
    }

    def __init__(self, *args, **kwargs):
        kwargs.pop('max_length')
        kwargs.pop('min_length')
        kwargs.pop('strip')
        super(CardSecurityCodeField, self).__init__(
            max_length=4,
            min_length=3,
            strip=True
        )
        self.validators.append(
            CardSecurityCodeValidator(
                self.error_messages['invalid'],
                code='invalid'
            )
        )
