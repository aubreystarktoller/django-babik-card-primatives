QUnit.test("buildCardNumberValidator", function(assert) {
    assert.strictEqual(buildCardNumberValidator()(''), null);
    assert.strictEqual(buildCardNumberValidator()('   '), null);

    assert.strictEqual(buildCardNumberValidator()('xxxx'), null);
    assert.strictEqual(buildCardNumberValidator()('42424242'), null);
    assert.strictEqual(buildCardNumberValidator()('HAHAHAHAHAHAHAHAHA'), null);
    assert.strictEqual(buildCardNumberValidator()('4242424242424242424242424242424242'), null);
    assert.strictEqual(buildCardNumberValidator()('444444444444444444'), null);
    assert.strictEqual(buildCardNumberValidator()('-4242-424242-424242   '), null);

    assert.strictEqual(buildCardNumberValidator()('424242424242424242'), '424242424242424242');
    assert.strictEqual(buildCardNumberValidator()(' 4242-424242-424242   '), '4242424242424242');


    assert.strictEqual(buildCardNumberValidator({required: false})(''), '');
    assert.strictEqual(buildCardNumberValidator({required: false})('   '), '');

    assert.strictEqual(buildCardNumberValidator({required: true})('   '), null);
    assert.strictEqual(buildCardNumberValidator({required: true})(''), null);
    assert.strictEqual(buildCardNumberValidator({required: true})('xxxx'), null);
    assert.strictEqual(buildCardNumberValidator({required: true})('42424242'), null);
    assert.strictEqual(buildCardNumberValidator({required: true})('HAHAHAHAHAHAHAHAHA'), null);
    assert.strictEqual(buildCardNumberValidator({required: true})('4242424242424242424242424242424242'), null);
    assert.strictEqual(buildCardNumberValidator({required: true})('444444444444444444'), null);
    assert.strictEqual(buildCardNumberValidator({required: true})('-4242-424242-424242   '), null);

    assert.strictEqual(buildCardNumberValidator({required: true})('424242424242424242'), '424242424242424242');
    assert.strictEqual(buildCardNumberValidator({required: true})(' 4242-424242-424242   '), '4242424242424242');
});
