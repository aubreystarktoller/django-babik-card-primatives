from django.test import TestCase, RequestFactory
from babik_card_primitives.fields import CARD_NUMBER_MAX_LENGTH
from tests.forms import CardNumberForm

class CardNumberFieldTestCase(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def _test_form_errors(self, data, errors=None):
        r = self.request_factory.post('/test', data)
        form = CardNumberForm(r.POST)
        if not errors:
            self.assertTrue(form.is_valid())
        else:
            self.assertFalse(form.is_valid())
            form_errors = form.errors['test_field'].as_data()
            self.assertEqual(set(e.code for e in form_errors), set(errors))

    def test_card_number_to_small(self):
        self._test_form_errors(
            {'test_field': '34'},
            ('min_length',)
        )

    def test_card_number_to_large(self):
        self._test_form_errors(
            {'test_field': '3434343434343434343434343434343434343434343434'},
            ('max_length',)
        )

    def test_card_number_invalid(self):
        self._test_form_errors(
            {'test_field': '472484934378784374'},
            ('invalid',)
        )

    def test_nonsense_card_number(self):
        self._test_form_errors(
            {'test_field': 'nonsense_card_no'},
            ('invalid',)
        )

    def test_empty_card_number(self):
        self._test_form_errors(
            {'test_field': ''},
            ('required',)
        )

    def test_card_number_valid(self):
        self._test_form_errors({'test_field': '49927398716'})

    def test_card_number_valid_with_whitespace(self):
        self._test_form_errors({'test_field': '4992 739 8716'})

    def test_widget_max_length(self):
        form = CardNumberForm()
        self.assertEqual(
            form.fields['test_field'].widget.attrs['maxlength'],
            str(CARD_NUMBER_MAX_LENGTH)
        )
