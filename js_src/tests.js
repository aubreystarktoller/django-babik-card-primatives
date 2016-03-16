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
        return (counter % 10 == 0);
    }
})();


/**
 * @function cardNumberLengthTest
 *
 * Tests the passed card number and ensures it is a vaugely sane
 * length. We're not to strict about the actual length, this is 
 * just to ensure that the card number is sane.
 *
 * @param cardNumber The card number to test
 */
var cardNumberLengthTest = (function() {
    var minLength = 10;
    var maxLength = 25;
  
    return function(cardNumber) {
        var temp = String(cardNumber);
        var len = temp.length;
        return minLength < len && len < maxLength;
    }

})();


/**
 * Tests the passed card number and ensures it's issuer is known.
 *
 * @param cardNumber The card number to test
 */
function cardNumberKnownIssuerTest(cardNumber) {
    return getCardIssuer(cardNumber) !== null;
}


/**
 * Tests the passed card number and ensures it's issuer is in a passed
 * whitelist
 *
 * @param cardNumber The card number to test
 * @param issuerWhiteList The issuers that are allowed
 */
function cardNumberIssuerWhitelistTest(cardNumber, issuerWhiteList) {
    var issuer = getCardIssuer(cardNumber);
    if (issuer !== null) {
        var len = issuerWhiteList.length;
        for (var i = 0; i < len; i++) {
            if(issuerWhiteList[i] == issuer) {
                return true;
            }
        }
    }
    return False;
}
