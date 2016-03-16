from django.test import TestCase
from babik_card_primitives.exceptions import (
    IssuerNotRecognised,
    InvalidCardNumber
)
from babik_card_primitives.utils import (
    get_card_issuer, 
    card_number_luhn_test,
    clean_card_number
)


class GetIssuerTestCase(TestCase):
    # card numbers taken from http://www.getcreditcardnumbers.com/

    def _test_card(self, number, expected_slug):
        slug, name = get_card_issuer(number)
        self.assertEqual(slug, expected_slug)

    def test_unknown(self):
        with self.assertRaises(IssuerNotRecognised):
            get_card_issuer('5')

    def test_visa16(self):
        self._test_card("4716492322141017", "visa")

    def test_visa13(self):
        self._test_card("4556119474911", "visa")

class CheckCardNumberTestCase(TestCase):
    def test_valid_numbers(self):
        self.assertTrue(card_number_luhn_test(1234567812345670))
        self.assertTrue(card_number_luhn_test(49927398716))

    def test_valid_numbers_as_strings(self):
        self.assertTrue(card_number_luhn_test("1234567812345670"))
        self.assertTrue(card_number_luhn_test("49927398716"))

    def test_invalid_number(self):
        self.assertFalse(card_number_luhn_test(1234567812345678))
        self.assertFalse(card_number_luhn_test(49927398717))

    def test_invalid_number_as_strings(self):
        self.assertFalse(card_number_luhn_test("1234567812345678"))
        self.assertFalse(card_number_luhn_test("49927398717"))


class CleanCardNumberTestCase(TestCase):
    def test_invalid_card_number(self):
        with self.assertRaises(InvalidCardNumber):
            clean_card_number("49927398716a")

    def test_strip_whitespace(self):
        clean_number = clean_card_number("4 992  7398	716")
        self.assertEqual(clean_number, "49927398716")
