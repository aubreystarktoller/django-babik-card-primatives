from django.forms import Form
from babik_card_primitives.fields import CardNumberField

class CardNumberForm(Form):
    test_field = CardNumberField()
