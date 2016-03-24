QUnit.test("getCardIssuer", function(assert) {
    assert.strictEqual(getCardIssuer("4716492322141017"), "visa");
    assert.strictEqual(getCardIssuer("4556119474911"), "visa");
    assert.strictEqual(getCardIssuer("5184304972563939"), "mastercard");

    assert.strictEqual(getCardIssuer("0000000000000"), null);
});


QUnit.test("partialApp", function(assert) {
    var buildTestFunc = function(tracker) {
        return function(arg1, arg2) {
            tracker.calledWith(arg1, arg2);   
        };
    };
    var tracker = new Tracker();
    var testFunc = buildTestFunc(tracker);

    var f= partialApp(testFunc, "test arg 1");
    f("test arg 2");
    assert.deepEqual(tracker.calls[0], ["test arg 1", "test arg 2"]);
});
