QUnit.test("cleanCardNumber", function(assert) {
    var test_invalid_cn = function(cn) {
        var validator =  new Validator(cleanCardNumber);
        validator.clean(cn);
        assert.deepEqual(validator.errors, ["invalid_card_number"])
    };

    var validator = new Validator(cleanCardNumber);
    assert.strictEqual(validator.clean("        1234  567812345678   "), "1234567812345678");
    assert.strictEqual(validator.clean("1234  5678123	45678"), "1234567812345678");
    assert.strictEqual(validator.clean("1234-567-8123-45678"), "1234567812345678");
    assert.strictEqual(validator.clean("1234-567-81 23-4 567	8"), "1234567812345678");

    test_invalid_cn("-1234-567-8123-45678");
    test_invalid_cn("1234-567-8123-45678-");
    test_invalid_cn("HAHAHAHA");
    test_invalid_cn("12HAHAHAHA34");
    test_invalid_cn(validator.clean("HAHAH12AH34A"));
});


QUnit.test("cleanCardSecurityCode", function(assert) {
    var test_invalid_cn = function(cn) {
        var validator =  new Validator(cleanCardSecurityCode);
        validator.clean(cn);
        assert.deepEqual(validator.errors, ["invalid_csc"])
    };

    var validator = new Validator(cleanCardSecurityCode);
    assert.strictEqual(validator.clean("        1234   "), "1234");
    assert.strictEqual(validator.clean("12 34"), "1234");
    assert.strictEqual(validator.clean(" 12 34 5"), "12345");

    test_invalid_cn("HAHAHAHA");
    test_invalid_cn("12HAHAHAHA34");
});
