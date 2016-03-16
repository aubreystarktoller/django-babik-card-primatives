class CardError(Exception):
    pass


class IssuerNotRecognised(CardError):
    pass


class InvalidCardNumber(CardError):
    pass
