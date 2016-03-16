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
