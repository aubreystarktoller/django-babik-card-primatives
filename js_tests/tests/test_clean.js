QUnit.test("cleanCardNumber", function(assert) {
    assert.strictEqual(cleanCardNumber("        1234  567812345678   "), "1234567812345678");
    assert.strictEqual(cleanCardNumber("1234  5678123	45678"), "1234567812345678");
    assert.strictEqual(cleanCardNumber("1234-567-8123-45678"), "1234567812345678");
    assert.strictEqual(cleanCardNumber("1234-567-81 23-4 567	8"), "1234567812345678");
    assert.strictEqual(cleanCardNumber("-1234-567-8123-45678"), null);
    assert.strictEqual(cleanCardNumber("1234-567-8123-45678-"), null);
    assert.strictEqual(cleanCardNumber("HAHAHAHA"), null);
    assert.strictEqual(cleanCardNumber("12HAHAHAHA34"), null);
    assert.strictEqual(cleanCardNumber("HAHAH12AH34A"), null);
});
