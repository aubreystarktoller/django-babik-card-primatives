QUnit.test("getCardIssuer", function(assert) {
    assert.strictEqual(getCardIssuer("4716492322141017"), "visa");
    assert.strictEqual(getCardIssuer("4556119474911"), "visa");
    assert.strictEqual(getCardIssuer("5184304972563939"), "mastercard");

    assert.strictEqual(getCardIssuer("0000000000000"), null);
});
