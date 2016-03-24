function Validator(cleanFunc, conf) {
    this.cleanFunc = cleanFunc;
    this.required = true;

    if (typeof conf === "undefined") {
        this.tests = Array();
    }
    else {
        if (typeof conf["required"] !== "undefined" && !conf["required"]) {
            this.required = false;
        }

        if (typeof conf["tests"] !== "undefined") {
            this.tests = conf["tests"];
        }
        else {
            this.tests = Array();
        }
    }

    this.errors = Array();
}


Validator.prototype.blankRegex = /^\s*$/;


/**
 * Adds an error to the validator if it hasn't already been added to the
 * validator - if it's already been set on the validator the error is not
 * added.
 *
 * @param errorSlug The error to add
 * @return {Boolean} Indicates whether the error was added or not
 */
Validator.prototype.addError = function(errorSlug) {
    var len = this.errors.length;
    if (!this.hasError(errorSlug)) {
        this.errors.push(errorSlug);
        return true;
    }
    else  {
        return false;
    }
}


/**
 * Removes an error to the validator if it is set on the validator
 *
 * @param errorSlug The error to remove
 * @return {Boolean} Indicates whether the error was removed or not
 */
Validator.prototype.removeError = function(errorSlug) {
    var len = this.errors.length;
    for (var i = 0; i < len; i++) {
        if (errorSlug == this.errors[i]) {
            this.errors.splice(i, 1)
            return true;
        }
    }
    return false;
}


/**
 * Tests whether or not an error is set on the validator
 *
 * @param errorSlug The error to look for
 * @return {Boolean} Indicates whether the error is present
 */
Validator.prototype.hasError = function(errorSlug) {
    var len = this.errors.length;
    for (var i = 0; i < len; i++) {
        if (errorSlug == this.errors[i]) {
            return true;
        }
    }
    return false;
}


/**
 * Addes a test to the validator
 *
 * @param test A function that takes cleaned value and returns a boolean
 * value indicating the validaty of the value
 * @param errorSlug The error slug to add to the validator in the event 
 * the test function returns false
 */
Validator.prototype.addTest = function(validator, errorSlug) {
    this.tests.push([validator, errorSlug]);
}


/**
 * Cleans the passed value
 */
Validator.prototype.clean = function(rawValue) {
    return this.cleanFunc(this, rawValue);
}


/**
 * Cleans and tests the passed value.
 *
 * @param rawValue the value to process 
 * @returns {Boolean} Returns a boolean indicating if the value is valid.
 * If it's invalid errors will be set on the validator.
 */
Validator.prototype.isValid = function(rawValue) {
    this.rawValue = rawValue;
    this.cleanValue = undefined;
    this.errors = Array();

    var strValue = String(rawValue);

    if (strValue.match(this.blankRegex) !== null) {
        this.cleanedValue = null;
        if (this.required) { 
            this.addError("required");
        }
    }
    else {
        this.cleanedValue = this.clean(strValue);
        if (this.errors.length == 0) {
            var len = this.tests.length;

            for (var i = 0; i < len; i++) {
                if (!this.tests[i][0](this.cleanedValue)) {
                    this.addError(this.tests[i][1]);
                }
            }
        }
    }
    return this.errors.length == 0;
}
