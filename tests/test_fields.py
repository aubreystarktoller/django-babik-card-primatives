from django.test import TestCase, RequestFactory
from django.core.exceptions import ValidationError

from testfixtures import LogCapture

from babik_card_primitives.two_field_date import TwoFieldDate
from babik_card_primitives.fields import (
    CARD_NUMBER_MAX_LENGTH,
    CardNumberField,
    CardSecurityCodeField,
    SensitiveChoiceField,
    TwoFieldDateField
)


class CardNumberFieldTestCase(TestCase):
    def test_card_number_to_small(self):
        field = CardNumberField()
        with self.assertRaises(ValidationError) as cm:
            field.clean("34")
        self.assertEqual(cm.exception.error_list[0].code, "min_length")

    def test_card_number_to_large(self):
        field = CardNumberField()
        with self.assertRaises(ValidationError) as cm:
            field.clean("3434343434343434343434343434343434343434343434")
        self.assertEqual(cm.exception.error_list[0].code, "max_length")

    def test_invalid_card_number(self):
        field = CardNumberField()
        with self.assertRaises(ValidationError) as cm:
            field.clean("472484934378784374")
        self.assertEqual(cm.exception.error_list[0].code, "invalid")

    def test_without_luhn(self):
        field = CardNumberField(use_luhn_test=False)
        field.clean("4000000000000000")

    def test_valid_issuer(self):
        field = CardNumberField(issuer_whitelist=['visa'])
        field.clean("4716492322141017")

    def test_invalid_issuer(self):
        field = CardNumberField(issuer_whitelist=['visa'])
        with self.assertRaises(ValidationError) as cm:
            field.clean("5184304972563939")
        self.assertEqual(cm.exception.error_list[0].code, "invalid_issuer")

    def test_nonsense_card_number(self):
        field = CardNumberField()
        with self.assertRaises(ValidationError) as cm:
            field.clean("nonsense card no")
        self.assertEqual(cm.exception.error_list[0].code, "invalid")

    def test_empty_card_number(self):
        field = CardNumberField()
        with self.assertRaises(ValidationError) as cm:
            field.clean("")
        self.assertEqual(cm.exception.error_list[0].code, "required")

    def test_valid_card_number(self):
        field = CardNumberField()
        field.clean("49927398716")

    def test_valid_card_number_with_whitespace(self):
        field = CardNumberField()
        field.clean("4992 7398 716")

    def test_valid_card_number_with_dashes(self):
        field = CardNumberField()
        field.clean("4992-7398-716")

    def test_valid_card_number_with_dashes_and_whitespace(self):
        field = CardNumberField()
        field.clean("4992-73 98-71 6")

    def test_invalid_dashed_card_number(self):
        field = CardNumberField()
        with self.assertRaises(ValidationError) as cm:
            field.clean("4992-73 98-71 6-")
        self.assertEqual(cm.exception.error_list[0].code, "invalid")

    def test_widget_max_length(self):
        field = CardNumberField()
        self.assertEqual(
            field.widget.attrs["maxlength"],
            str(CARD_NUMBER_MAX_LENGTH)
        )

    def test_widget_client_side_only(self):
        field = CardNumberField(client_side_only=True)
        self.assertTrue(field.widget.attrs["client_side_only"])

    def test_client_side_only_with_data(self):
        field = CardNumberField(client_side_only=True)
        with LogCapture("babik_card_primatives") as l:
            field.clean("49927398716")

        l.check(
            (
                "babik_card_primatives",
                "CRITICAL",
                "Data that should not have reached the server has reached the server."
            ),
        )


class CSCFieldTestCase(TestCase):
    def test_valid_csc(self):
        field = CardSecurityCodeField()
        field.clean("4444")

    def test_valid_csc_with_whitespace(self):
        field = CardSecurityCodeField()
        field.clean("    4444    ")

    def test_invalid_csc(self):
        field = CardSecurityCodeField()
        with self.assertRaises(ValidationError) as cm:
            field.clean("xxxx")
        self.assertEqual(cm.exception.error_list[0].code, 'invalid_csc')

    def test_csc_to_python_with_none_value(self):
        field = CardSecurityCodeField()
        self.assertEqual(field.to_python(None), '')

    def test_csc_to_python_with_empty_string_value(self):
        field = CardSecurityCodeField()
        self.assertEqual(field.to_python('   '), '')

    def test_client_side_only_with_data(self):
        field = CardSecurityCodeField(client_side_only=True)
        with LogCapture("babik_card_primatives") as l:
            field.clean('test1')

        l.check(
            (
                "babik_card_primatives",
                "CRITICAL",
                "Data that should not have reached the server has reached the server."
            ),
        )

    def test_widget_client_side_only_attr(self):
        field = CardSecurityCodeField(client_side_only=True)
        self.assertIn('client_side_only', field.widget.attrs)


class SensitiveChoiceFieldTestCase(TestCase):
    CHOICES = (
        ('test1', 'Test 1'),
        ('test2', 'Test 2'),
    )

    def test_client_side_only_with_data(self):
        field = SensitiveChoiceField(choices=self.CHOICES)
        with LogCapture("babik_card_primatives") as l:
            field.clean()
        l.check()

    def test_client_side_only_with_data(self):
        field = SensitiveChoiceField(choices=self.CHOICES, client_side_only=True)
        with LogCapture("babik_card_primatives") as l:
            field.clean('test1')

        l.check(
            (
                "babik_card_primatives",
                "CRITICAL",
                "Data that should not have reached the server has reached the server."
            ),
        )

    def test_valid_data(self):
        field = SensitiveChoiceField(choices=self.CHOICES)
        field.clean('test1')

    def test_invalid_data(self):
        field = SensitiveChoiceField(choices=self.CHOICES)
        with self.assertRaises(ValidationError) as cm:
            field.clean('test3')
        self.assertEqual(cm.exception.code, 'invalid_choice')

    def test_widget_client_side_only_attr(self):
        field = SensitiveChoiceField(choices=self.CHOICES, client_side_only=True)
        self.assertIn('client_side_only', field.widget.attrs)


class TwoFieldDateFieldTestCase(TestCase):
    def test_to_python_with_empty_string_value(self):
        field = TwoFieldDateField()
        self.assertIsNone(field.to_python(''))

    def test_to_python_with_none_value(self):
        field = TwoFieldDateField()
        self.assertIsNone(field.to_python(None))

    def test_to_python_with_two_field_date_value(self):
        field = TwoFieldDateField()
        tfd = TwoFieldDate(2016, 10)
        self.assertEqual(field.to_python(tfd), tfd)

    def test_to_python_with_valid_dict(self):
        field = TwoFieldDateField()
        self.assertEqual(
            field.to_python({'year': "2016", "month": "10"}),
            TwoFieldDate(2016, 10)
        )

    def test_to_python_with_dict_with_non_int_month(self):
        field = TwoFieldDateField()
        with self.assertRaises(ValidationError) as cm:
            field.to_python({'year': "2016", "month": "x"})
        self.assertEqual(cm.exception.code, "invalid_month")

    def test_to_python_with_dict_with_0_month(self):
        field = TwoFieldDateField()
        with self.assertRaises(ValidationError) as cm:
            field.to_python({'year': "2016", "month": "0"})
        self.assertEqual(cm.exception.code, "invalid_month")

    def test_to_python_with_dict_with_negative_month(self):
        field = TwoFieldDateField()
        with self.assertRaises(ValidationError) as cm:
            field.to_python({'year': "2016", "month": "-1"})
        self.assertEqual(cm.exception.code, "invalid_month")

    def test_to_python_with_dict_with_to_large_month(self):
        field = TwoFieldDateField()
        with self.assertRaises(ValidationError) as cm:
            field.to_python({'year': "2016", "month": "15"})
        self.assertEqual(cm.exception.code, "invalid_month")

    def test_to_python_with_dict_with_to_string_year(self):
        field = TwoFieldDateField()
        with self.assertRaises(ValidationError) as cm:
            field.to_python({'year': "x", "month": "12"})
        self.assertEqual(cm.exception.code, "invalid_year")

    def test_widget_client_side_only_attr(self):
        field = TwoFieldDateField(client_side_only=True)
        self.assertIn('client_side_only', field.widget.attrs)

    def test_client_side_only_with_data(self):
        field = TwoFieldDateField(client_side_only=True)
        with LogCapture("babik_card_primatives") as l:
            field.clean('test')

        l.check(
            (
                "babik_card_primatives",
                "CRITICAL",
                "Data that should not have reached the server has reached the server."
            ),
        )

    def test_to_python_with_string_value_and_default_input_format(self):
        field = TwoFieldDateField()
        self.assertEqual(
            field.to_python("102016"),
            TwoFieldDate(2016, 10)
        )

    def test_to_python_with_string_value_and_set_input_format(self):
        field = TwoFieldDateField(input_formats=["%m-%Y"])
        self.assertEqual(
            field.to_python(" 9-2016"),
            TwoFieldDate(2016, 9)
        )

    def test_to_python_with_string_value_and_no_matchin_input_format(self):
        field = TwoFieldDateField(input_formats=["%m%Y"])
        with self.assertRaises(ValidationError) as cm:
            field.to_python(" 9-2016"),
        self.assertEqual(cm.exception.code, "invalid")

    def test_set_input_formats(self):
        field = TwoFieldDateField()
        field.input_formats = ["test"]
        self.assertEqual(field.input_formats, ["test"])
