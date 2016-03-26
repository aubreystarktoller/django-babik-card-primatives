function TwoFieldDate(year, month) {
    this.month = month;
    this.year = year;
}


function TwoFieldDateStrParser(format) {
    this.rawFormat = format;

    this.formatErrors = Array();
    this.mapper = Array();

    this.monthDirectiveFound = false;
    this.yearDirectiveFound = false;

    var inner = format.split("%%").map(this.buildRegex, this).join("%");

    if (this.monthDirectiveFound && this.yearDirectiveFound) {
        this.regex = RegExp("^" + inner + "$", "i");
        this.mapperLength = mapper.length;
    }
    else {
        this.addFormatError(
            'Both a year directive and a month directive must be specified'
        );
    }
}
  

TwoFieldDateStrParser.prototype.abbrMonths = [
    "jan", "feb", "mar", "apr", "may", "jun",
    "jul", "aug", "sep", "oct", "nov", "dec"
]


TwoFieldDateStrParser.prototype.months = [
    "january", "february", "march",
    "april", "may", "june",
    "july", "august", "september",
    "october", "november", "december",
]


TwoFielDateStrParser.prototype.directiveToRegex = {
    "b": "(" + abbrMonths.join("|") + ")",
    "B": "(" + months.join("|") + ")",
    "m": "([0 ]?[1-9]|1[0-2])",
    "y": "([0-9]{2})",
    "Y": "([0-9]{4})",
}


TwoFieldDateStrParser.prototype.directiveRegex = RegExp("%[bBmyY]");


TwoFieldDateStrParser.prototype.strayDirectiveRegex = RegExp("%(.)");


TwoFieldDateStrParser.prototype.monthToInt = function(month) {
    var temp = month.toLowerCase();
    for (var i = 0; i < 12; i++) {
        if (temp == months[i]) {
            return i;
        }
    }
    return null;
}


TwoFieldDateStrParser.prototype.abbrMonthToInt = function(month) {
    var temp = abbrMonth.toLowerCase();
    for (var i = 0; i < 12; i++) {
        if (temp == abbrMonths[i]) {
            return i;
        }
    }
    return null;
}


TwoFieldDateStrParser.prototype.addFormatError = function(error) {
    this.formatErrors.push(error);
}


TwoFieldDateStrParser.prototype.addParseError = function(error) {
    this.parseErrors.push(error);
}


TwoFieldDateStrParser.prototype.parseDirective = function(match, directive) {
    this.mapper.push(directive);
    if directive == 'b' || directive == 'B' || directive == 'm':
        this.monthDirectiveFound = true;
    else {
        this.yaerDirectiveFound = true;
    }
    return this.directiveToRegex[directive];
}


TwoFieldDateStrParser.prototype.buildRegex = function(format) {
    var temp = parts[i].replace(directiveRegex, parseDirective);
    var match = temp.match(strayDirective);

    if (match) {
        this.addFormatError(
            '"' + match[0] + '" is a bad directive in format string "' + this.rawFormat + '"'
        )
    }
    else {
        return temp;
    }
}


TwoFieldDateStrParser.prototype.parse = function(str) {
    this.parseErrors = Array();
    var match = str.match(this.regex);

    if (match) {
        var month = null;
        var year = null;

        for (var i = 0; i < this.mapperLength; i++) {
            switch(this.mapper[i]) {
                case 'b':
                    var temp = abbrMonthToInt(match[i]);
                    if (month !== null && temp !== month) {
                        this.addParseError(
                            'Mutltiple, dfferent month values are given.'
                        )
                    }
                    else {
                        month = temp;
                    }
                    break;
                case 'B':
                    var temp = monthToInt(match[i]);
                    if (month !== null && temp !== month) {
                        this.addParseError(
                            'Mutltiple, dfferent month values are given.'
                        )
                    }
                    else {
                        month = temp;
                    }
                    break;
                case 'm':
                    var temp = monthToInt(match[i]);
                    if (month !== null && temp !== month) {
                        this.addParseError(
                            'Mutltiple, dfferent month values are given.'
                        )
                    }
                    else {
                        month = temp;
                    }
                    break;
                case 'y':
                    var partialYear = parseInt(match[i]);

                    var temp;
                    if (partialYear < 69) {
                        temp = partialYear + 2000;
                    }
                    else {
                        temp = partialYear + 1900;
                    }

                    if (year !== null && year !== temp) {
                         this.addParseError(
                            'Mutltiple, different year values are given'
                         )
                    }
                    else {
                        year = temp;
                    }
                    break;
                case 'Y':
                    var temp = parseInt(match[i]);
                    if (year !== null && year !== temp) {
                        this.addParseError(
                            'Mutltiple, different year values are given'
                        )
                    }
                    else {
                        year = temp;
                    }
                    break;
            }
        }

        return TwoFieldDate(year, month);
    }
    else {
        this.addParseError(
           'string "' + str + '" does not match format string "' + this.rawFormat + '"'
        )
    }
}
