/**
 * Function that builds a validator for a card number,
 *
 * @param {Object} conf Configures the validator
 * @param {boolean} conf.required Boolean value indicating if the card
 * number is required or not. If not set defaults to true.
 * @param {string[]} conf.issuser_whitelist A whitelist of allowed issuers. If 
 * omitted the card issuser is not checked.
 */
function buildCardNumberValidator(conf) {
    validator = new Validator(cleanCardNumber);

    validator.addTest(partialApp(minLengthTest, 10), "card_number_to_short");
    validator.addTest(curreyFunc(maxLengthTest, 25), "card_number_to_long");
    validator.addValue(cardNumberLuhnTest, "card_number_invalid");

    if (typeof conf !== 'undefined') {
        if (typeof conf.required !== "undefined" && !conf.required) {
            validator.required = false;
        }

        if (typeof conf.issuerWhitelist !== "undefined") {
            validator.addValidator(
                partialApp(
                    cardNumberIssuerWhitelistTest,
                    conf.issuer_whitelist,
                ),
                "invalid_issuer"
            );
        }
    }

    return validator;
}


/**
 * Function that builds a validator for a card secuirty code.
 *
 * @param {Object} conf Configures the validator
 * @param {boolean} conf.required Boolean value indicating if the card
 * security code is required or not. If not set defaults to true.
 */
function buildCardSeurirtCodeValidator(conf) {
    var validator = new Validator(cleanCardSecurityCode);

    if (typeof conf !== 'undefined') {
        if (typeof conf.required !== "undefined" && !conf.required) {
            validator.required = false;
        }
    }

    validator.addTest(partialApp(minLengthTest, 3), "csc_number_to_short");
    validator.addTest(partialApp(maxLengthTest, 4), "csc_number_to_long");

    return validator;
}
