QUnit.test("cardNumberLuhnTest", function(assert) {
    assert.strictEqual(cardNumberLuhnTest(1234567812345670), true);
    assert.strictEqual(cardNumberLuhnTest(49927398716), true);
        
    assert.strictEqual(cardNumberLuhnTest("1234567812345670"), true);
    assert.strictEqual(cardNumberLuhnTest("49927398716"), true);

    assert.strictEqual(cardNumberLuhnTest(1234567812345678), false);
    assert.strictEqual(cardNumberLuhnTest(49927398717), false);
        
    assert.strictEqual(cardNumberLuhnTest("1234567812345678"), false);
    assert.strictEqual(cardNumberLuhnTest("49927398717"), false);
});


QUnit.test("cardNumberLengthTest", function(assert) {
    assert.strictEqual(cardNumberLengthTest('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'), false);
    assert.strictEqual(cardNumberLengthTest('xxxxx'), false);
    assert.strictEqual(cardNumberLengthTest('xxxxxxxxxxxxxxxxxxx'), true);
});


QUnit.test("cardNumberIssuerWhitelistTest", function(assert) {
    assert.strictEqual(cardNumberIssuerWhitelistTest("4716492322141017", ["visa"]), true);
    assert.strictEqual(cardNumberIssuerWhitelistTest("0000000000000000", ["visa"]), false);
});
