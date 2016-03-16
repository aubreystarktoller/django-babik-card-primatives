from django.test import TestCase
from django.core.exceptions import ValidationError
from babik_card_primatives.validators import CardNumberValidator


class CardNumberValidatorTestCase(TestCase):
    def test_nonsense_card_number(self):
        validator = CardNumberValidator()
        with self.assertRaises(ValidationError) as cm:
            validator("nonsense")
        self.assertEqual(cm.exception.code, "invalid_card_number")

    def test_nonsense_card_number_with_set_code(self):
        validator = CardNumberValidator(code = "test")
        with self.assertRaises(ValidationError) as cm:
            validator("nonsense")
        self.assertEqual(cm.exception.code, "test")

    def test_nonsense_card_number_with_set_message(self):
        validator = CardNumberValidator(message = "test")
        with self.assertRaises(ValidationError) as cm:
            validator("nonsense")
        self.assertEqual(cm.exception.message, "test")

    def test_invalid_card_number(self):
        validator = CardNumberValidator()
        with self.assertRaises(ValidationError) as cm:
            validator("49927398717")
        self.assertEqual(cm.exception.code, "invalid_card_number")

    def test_invalid_card_number_with_set_code(self):
        validator = CardNumberValidator(code="test")
        with self.assertRaises(ValidationError) as cm:
            validator("49927398717")
        self.assertEqual(cm.exception.code, "test")

    def test_invalid_card_number_with_set_message(self):
        validator = CardNumberValidator(message="test")
        with self.assertRaises(ValidationError) as cm:
            validator("49927398717")
        self.assertEqual(cm.exception.message, "test")

    def test_valid_card_number(self):
        validator = CardNumberValidator()
        validator("49927398716")
