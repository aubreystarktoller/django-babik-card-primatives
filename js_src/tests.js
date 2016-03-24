/**
 * @function cardNumberLuhnTest
 *
 * Tests the passed card number using Luhn's algorithm.
 *
 * @param cardNumber The card number to test
 */
var cardNumberLuhnTest = (function() {
    var luhnConversion = [0, 2, 4, 6, 8, 1, 3, 5, 7, 9];

    return function(cardNumber) {
        var counter = 0;
        var n;
        var odd = true;
        var temp = String(cardNumber);

        for (var i = temp.length - 1; i >= 0; --i) {
            n = parseInt(temp.charAt(i), 10);
            if (odd) {
                counter += n;
            }
            else {
                counter += luhnConversion[n];
            }
            odd = !odd;
        }
        return (counter % 10 === 0);
    }
})();


/**
 * Compare the passed value's length to maximum allowed length.
 *
 * @param max The maximum length allowed
 * @param valuer The cleaned value to test
 */
function maxLengthTest(max, value) {
      return value.length <= max;
}


/**
 * Compare the passed value's length to minimum allowed length.
 *
 * @param min The minimum length allowed
 * @param valuer The cleaned value to test
 */
function minLengthTest(min, value) {
      return value.length >= min;
}


/**
 * Tests the passed card number and ensures it's issuer is known.
 *
 * @param cardNumber The cleaned card number (a card number returned by
 * cleanCardNumber) to test
 */
function cardNumberKnownIssuerTest(cardNumber) {
    return getCardIssuer(cardNumber) !== null;
}


/**
 * Tests the passed card number and ensures it's issuer is in a passed
 * whitelist
 *
 * @param cardNumber The cleaned card number (a card number returned by
 * cleanCardNumber) to test
 * @param issuerWhiteList The issuers that are allowed
 */
function cardNumberIssuerWhitelistTest(issuerWhiteList, cardNumber) {
    var issuer = getCardIssuer(cardNumber);
    if (issuer !== null) {
        var len = issuerWhiteList.length;
        for (var i = 0; i < len; i++) {
            if(issuerWhiteList[i] === issuer) {
                return true;
            }
        }
    }
    return false;
}
