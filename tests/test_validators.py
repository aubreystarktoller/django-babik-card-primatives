from django.test import TestCase
from django.core.exceptions import ValidationError
from babik_card_primitives.validators import (
    CardNumberLuhnTestValidator,
    CardNumberIssuerWhitelistValidator,
    CardSecurityCodeValidator
)


class CardNumberLuhnTestValidatorTestCase(TestCase):
    def test_nonsense_card_number(self):
        validator = CardNumberLuhnTestValidator()
        with self.assertRaises(ValidationError) as cm:
            validator("nonsense")
        self.assertEqual(cm.exception.code, "invalid_card_number")

    def test_nonsense_card_number_with_set_code(self):
        validator = CardNumberLuhnTestValidator(code = "test")
        with self.assertRaises(ValidationError) as cm:
            validator("nonsense")
        self.assertEqual(cm.exception.code, "test")

    def test_nonsense_card_number_with_set_message(self):
        validator = CardNumberLuhnTestValidator(message = "test")
        with self.assertRaises(ValidationError) as cm:
            validator("nonsense")
        self.assertEqual(cm.exception.message, "test")

    def test_invalid_card_number(self):
        validator = CardNumberLuhnTestValidator()
        with self.assertRaises(ValidationError) as cm:
            validator("49927398717")
        self.assertEqual(cm.exception.code, "invalid_card_number")

    def test_invalid_card_number_with_set_code(self):
        validator = CardNumberLuhnTestValidator(code="test")
        with self.assertRaises(ValidationError) as cm:
            validator("49927398717")
        self.assertEqual(cm.exception.code, "test")

    def test_invalid_card_number_with_set_message(self):
        validator = CardNumberLuhnTestValidator(message="test")
        with self.assertRaises(ValidationError) as cm:
            validator("49927398717")
        self.assertEqual(cm.exception.message, "test")

    def test_valid_card_number(self):
        validator = CardNumberLuhnTestValidator()
        validator("49927398716")


class CardSecurityCodeValidatorTestCase(TestCase):
    def test_valid_csc_length_3(self):
        CardSecurityCodeValidator()("444")

    def test_valid_csc_length_4(self):
        CardSecurityCodeValidator()("4444")

    def test_invalid_csc(self):
        with self.assertRaises(ValidationError) as cm:
            CardSecurityCodeValidator()("HAHAHA")
        self.assertEqual(cm.exception.code, "invalid_csc")

    def test_invalid_csc_with_set_code(self):
        with self.assertRaises(ValidationError) as cm:
            CardSecurityCodeValidator(code='test')("HAHAHA")
        self.assertEqual(cm.exception.code, "test")

    def test_invalid_csc_with_set_message(self):
        with self.assertRaises(ValidationError) as cm:
            CardSecurityCodeValidator(message="test")("HAHAHA")
        self.assertEqual(cm.exception.message, "test")


class CardNumberIssuerWhitelistValidatorTestCase(TestCase):
    def test_valid(self):
        CardNumberIssuerWhitelistValidator(["visa"])("4716492322141017")

    def test_invalid(self):
        with self.assertRaises(ValidationError) as cm:
            CardNumberIssuerWhitelistValidator(["visa"])("5716492322141017")
        self.assertEqual(cm.exception.code, "invalid_issuer")

    def test_invalid_with_set_code(self):
        with self.assertRaises(ValidationError) as cm:
            CardNumberIssuerWhitelistValidator(["visa"], code="test")("5716492322141017")
        self.assertEqual(cm.exception.code, "test")

    def test_invalid_with_set_message(self):
        with self.assertRaises(ValidationError) as cm:
            CardNumberIssuerWhitelistValidator(["visa"], message="test")("5716492322141017")
        self.assertEqual(cm.exception.message, "test")

    def test_invalid_with_whitelist_miss(self):
        with self.assertRaises(ValidationError) as cm:
            CardNumberIssuerWhitelistValidator(["mastercard"])("4716492322141017")
        self.assertEqual(cm.exception.code, "invalid_issuer")
