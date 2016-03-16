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
    ];
    var cardIssuerLen = cardIssuers.length;

    return function(cardNumber) {
        var result;
        var issuerData;

        for(var i = 0;  i < cardIssuerLen; i++) {
            issuerData = cardIssuers[i];
            result = issuerData[0].match(cardNumber);
            if (result !== null) {
                return [issuerData[1], issuerData[2]];
            }
        }
        return null;
    }
})();
