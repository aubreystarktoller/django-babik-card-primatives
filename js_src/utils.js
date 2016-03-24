/**
 * @function getCardIssuer
 *
 * Matches a card number against the card numbers issued by known
 * issuers and returns the matching issuer.
 *
 * @param cardNumber The card number to test
 */
var getCardIssuer = (function() {
    var cardIssuers = [
        [/^5[1-5][0-9]{14}$/, "mastercard"],
        [/^4[0-9]{12,19}$/, "visa"]
    ];
    var cardIssuerLen = cardIssuers.length;

    return function(cardNumber) {
        var result;
        var issuerData;

        for(var i = 0; i < cardIssuerLen; i++) {
            issuerData = cardIssuers[i];
            result = cardNumber.match(issuerData[0]);
            if (result !== null) {
                return issuerData[1];
            }
        }
        return null;
    };
})();


/**
 * Partially apply some of a functions arguments
 *
 * @param func The function whose arguments are to be set
 * @param {...*} The arguments to apply to the function
 */
function partialApp(f) {
    var parameters = Array.prototype.slice.call(arguments, 1);

    return function() {
        return f.apply(
            this,
            parameters.concat(Array.prototype.slice.call(arguments, 0))
        );
    };
}
