import re
from babik_card_primitives.exceptions import (
    InvalidCardNumber,
    IssuerNotRecognised
)


CARD_ISSUERS = [
]


def get_card_issuer(number):
    """
    Use a card's ... to determine it's issuer
    """
    number = str(number)
    for regexp, issuer_slug, issuer_name in CARD_ISSUERS:
        if re.match(regexp, number):
            return issuer_slug, issuer_name
    raise IssuerNotRecognised()


def check_card_number(number):
    """
    Use Luhn's algorithm to varify a credit card number
    """
    reverse_digit_list = [int(n) for n in str(number)][::-1]
    odd_sum = sum(n for n in reverse_digit_list[0::2])
    even_sum = sum(sum(divmod(n * 2, 10)) for n in reverse_digit_list[1::2])
    return (odd_sum + even_sum) % 10 == 0


whitespace_re = re.compile('\s+')
card_number_re = re.compile('^[0-9]+$')


def clean_card_number(raw_number):
    """
    Removes any whitespace from a card number, throws an InvalidCardNumber if
    there are not numeric characters remaining
    """
    number = whitespace_re.sub('', raw_number)
    if card_number_re.match(number):
        return number
    else:
        raise InvalidCardNumber
