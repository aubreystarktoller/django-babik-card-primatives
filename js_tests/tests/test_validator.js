function clean(tracker) {
    return "test_clean";
}


function positiveTest(cleanedValue) {
    return true;
}


function negativeTest(cleanedValue) {
    return false;
}


QUnit.test("Validator defaults", function(assert) {
    var validator = new Validator(clean);
    assert.strictEqual(validator.required, true);
    assert.ok(Array.isArray(validator.tests) && validator.tests.length == 0);
    assert.ok(Array.isArray(validator.errors) && validator.errors.length == 0);
});


QUnit.test("Validator with required in conf", function(assert) {
    var validator = new Validator(clean, {"required": false});
    assert.strictEqual(validator.required, false);

    var tracker = new Tracker();
    var validator = new Validator(clean, {"required": true});
    assert.strictEqual(validator.required, true);
});


QUnit.test("Validator with tests in conf", function(assert) {
    var validator = new Validator(clean, {"tests": [[positiveTest, "test"]]});
    assert.deepEqual(validator.tests, [[positiveTest, "test"]]);
});


QUnit.test("Validator.addError", function(assert) {
    var validator = new Validator(clean);

    assert.ok(validator.addError("test"));
    assert.deepEqual(validator.errors, ['test'])

    assert.ok(validator.addError("test1"));
    assert.deepEqual(validator.errors, ["test", "test1"])

    assert.notOk(validator.addError("test"));
    assert.deepEqual(validator.errors, ["test", "test1"])
});


QUnit.test("Validator.hasError", function(assert) {
    var validator = new Validator(clean);
    validator.errors.push("test");
    assert.ok(validator.hasError("test"));
    assert.notOk(validator.hasError("test1"));
});


QUnit.test("Validator.removeError", function(assert) {
    var validator = new Validator(clean);

    assert.notOk(validator.removeError("test1"));

    validator.errors.push("test");
    assert.ok(validator.removeError("test"));

    assert.notOk(validator.removeError("test"));
});


QUnit.test("Validator.addTest", function(assert) {
    var validator = new Validator(clean);

    validator.addTest(positiveTest, "error_slug");
    assert.deepEqual(validator.tests, [[positiveTest, "error_slug"]]);

    validator.addTest(positiveTest, "error_slug");
    assert.deepEqual(validator.tests, [[positiveTest, "error_slug"], [positiveTest, "error_slug"]]);
});


QUnit.test("Validator.isValid with no tests", function(assert) {
    var validator = new Validator(clean);

    r = validator.isValid("test");
    assert.strictEqual(r, true);
});


QUnit.test("Validator.isValid with tests", function(assert) {
    var validator = new Validator(clean, {"tests": [[negativeTest, "error"]]});

    r = validator.isValid("test");
    assert.strictEqual(r, false);

    assert.deepEqual(validator.errors, ["error"]);
});


QUnit.test("Validator.isValid with empty value", function(assert) {
    var validator = new Validator(clean);

    r = validator.isValid(" ");
    assert.strictEqual(r, false);
});


QUnit.test("Validator.isValid with required false and empty value", function(assert) {
    var validator = new Validator(clean, {"required": false});

    r = validator.isValid(" ");
    assert.strictEqual(r, true);
});


QUnit.test("Validator.isValid with required true and empty value", function(assert) {
    var validator = new Validator(clean, {"required": true});

    r = validator.isValid(" ");
    assert.strictEqual(r, false);
});
