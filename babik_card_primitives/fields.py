from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from django.forms.fields import Field
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text

from babik_card_primitives.exceptions import InvalidCardNumber
from babik_card_primitives.utils import clean_card_number
from babik_card_primitives.validators import CardNumberValidator


CARD_NUMBER_MIN_LENGTH = 10
CARD_NUMBER_MAX_LENGTH = 25


class CardNumberField(Field):
    default_error_messages = {
        'invalid': _('Invalid card number'),
    }

    def __init__(self, *args, **kwargs):
        super(CardNumberField, self).__init__(*args, **kwargs)

        min_validator = MinLengthValidator(CARD_NUMBER_MIN_LENGTH)
        max_validator = MaxLengthValidator(CARD_NUMBER_MAX_LENGTH)
        card_number_validator = CardNumberValidator(
            self.error_messages['invalid'],
            code='invalid'
        )

        self.validators.append(min_validator)
        self.validators.append(max_validator)
        self.validators.append(card_number_validator)

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
        attrs.update({'maxlength': str(CARD_NUMBER_MAX_LENGTH)})
        return attrs
