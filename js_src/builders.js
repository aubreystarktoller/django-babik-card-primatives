/**
 * Wrapper around cardNumberWhitelistTest that returns a function that
 * takes only a card number as a parameter (issuerWhiteList becomes a closure
 * variable).
 *
 * @param issuerWhiteList The issuers that are allowed
 */
function buildCardNumberIssuerWhitelistTest(issuerWhiteList) {
    return function(cardNumber) {
        return cardNumberIssuerWhitelistTest(cardNumber, issuerWhiteList);
    }
}


/**
 * Function that builds a function that takes a raw inputed card number,
 * cleans it, validates it and either returns: null if the inputed value
 * wad invalid; a cleanded card number if one was input and it was valid;
 * a empty string if there was no data input and no value was required.
 *
 * @param {Object} conf Configuresthe validator
 * @param {boolean} conf.required Boolean value indicating if the card
 * number is required or not. If not set defaults to true.
 * @param {string[]} conf.issuser_whitelist A whitelist of allowed issuers. If 
 * omitted the card issuser is not checked.
 */
function buildCardNumberValidator(conf) {
    var validators = [
        cardNumberLengthTest,
        cardNumberLuhnTest,
    ]
    var whitespaceRegex = /^\s*$/;
    var required = true;

    if (typeof conf !== 'undefined') {
        if (typeof conf.required !== "undefined" && !conf.required) {
            required = false;
        }

        if (typeof conf.issuerWhitelist !== "undefined") {
            var v = buildCardNumberIssuerWhitelistTest(conf.issuer_whitelist);
            validators.push(v);
        }
    }

    var len = validators.length;

    return function(cardNumber) {
        var temp = String(cardNumber);
        if(temp.match(whitespaceRegex) !== null) {
            if (required) { 
                return null;
            }
            else {
                return '';
            }
        }
        else {
            temp = cleanCardNumber(cardNumber);
            for (var i = 0; i < len; i++) {
                if (!validators[i](temp)) {
                    return null;
                }
            }
            return temp;
        }
    }
}
