QUnit.test("cardNumberLuhnTest", function(assert) {
    assert.strictEqual(cardNumberLuhnTest("1234567812345670"), true);
    assert.strictEqual(cardNumberLuhnTest("49927398716"), true);

    assert.strictEqual(cardNumberLuhnTest("1234567812345678"), false);
    assert.strictEqual(cardNumberLuhnTest("49927398717"), false);
});


QUnit.test("maxLengthTest", function(assert) {
    assert.strictEqual(maxLengthTest(6, 'xxxxxx'), true);
    assert.strictEqual(maxLengthTest(2, 'xxxxx'), false);
});


QUnit.test("minLengthTest", function(assert) {
    assert.strictEqual(minLengthTest(4, 'xxxxxx'), true);
    assert.strictEqual(minLengthTest(10, 'xxxxx'), false);
});


QUnit.test("cardNumberIssuerWhitelistTest", function(assert) {
    assert.strictEqual(cardNumberIssuerWhitelistTest(["visa"], "4716492322141017"), true);
    assert.strictEqual(cardNumberIssuerWhitelistTest(["visa"], "0000000000000000"), false);
});
