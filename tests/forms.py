from django.forms import Form
from babik_card_primatives.fields import CardNumberField

class CardNumberForm(Form):
    test_field = CardNumberField()
