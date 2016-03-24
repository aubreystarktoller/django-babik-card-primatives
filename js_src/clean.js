/**
 * @function cleanCardNumber
 *
 * Removes whitespace and dashes from a card number. Returns null if the
 * cleaned value doesn't look like a card number.
 *
 * @param cardNumber The card number to clean
 */
var cleanCardNumber = (function() {
    var whitespaceRegex = /[\s+]+/g;
    var dashRegex = /([0-9])-([0-9])/g;
    var finalCardNumberRegex = /^[0-9]+$/;

    return function(validator, cardNumber) {
        var temp = String(cardNumber);
        temp = temp.replace(whitespaceRegex, "");
        temp = temp.replace(dashRegex, "$1$2");
        var result = temp.match(finalCardNumberRegex);
        if (result) {
            return temp;
        }
        else {
            validator.addError("invalid_card_number");
        }
    };
})();


/**
 * @function cleanCardSecurityCode
 *
 * Removes whitespace from a card security code. Returns null if the
 * cleaned value doesn't look like a card security.
 *
 * @param cardSecurityCode The card secuirty code to clean
 */
var cleanCardSecurityCode = (function() {
    var whitespaceRegex = /[\s+]+/g;
    var finalCardSecurityCodeRegex = /^[0-9]+$/;

    return function(validator, cardSecurityCode) {
        var temp = String(cardSecurityCode);
        temp = temp.replace(whitespaceRegex, "");
        var result = temp.match(finalCardSecurityCodeRegex);
        if (result) {
            return temp;
        }
        else {
            validator.addError("invalid_csc");
        }
    };
})();
