function TwoFieldDate(year, month) {
    this.month = month;
    this.year = year;
}


var strToTwoFieldDate = (function() {
    var abbrMonths = [
        "jan", "feb", "mar", "apr", "may", "jun",
        "jul", "aug", "sep", "oct", "nov", "dec"
    ]
    var months = [
        "january", "february", "march",
        "april", "may", "june",
        "july", "august", "september",
        "october", "november", "december",
    ]

    var monthToInt = function(month) {
        var temp = month.toLowerCase();
        for (var i = 0; i < 12; i++) {
            if (temp == months[i]) {
                return i;
            }
        }
        return null;
    }

    var abbrMonthToInt = function(abbrMonth) {
        var temp = abbrMonth.toLowerCase();
        for (var i = 0; i < 12; i++) {
            if (temp == abbrMonths[i]) {
                return i;
            }
        }
        return null;
    }

    var directiveRegex = {
        "b": "(" + abbrMonths.join("|") + ")",
        "B": "(" + months.join("|") + ")",
        "m": "([0 ]?[1-9]|1[0-2])",
        "y": "([0-9]{2})",
        "Y": "([0-9]{4})",
    }
    var directives = ["b", "B", "m", "y", "Y"];
    var directivesLen = directives.length;

    var strayDirectiveRegex = RegExp("%(.)");

    return function(str, format) {
        var parts = format.split("%%");
        var convertedParts = Array();
        var len = parts.length;
        var mapper = Array();

        for (var i = 0; i < len; i++) {
            var temp = parts[i];
            for (var j = 0; j < directivesLen; j++) {
                var d = directives[j];
                if (temp.includes("%" + d)) {
                    temp = temp.replace("%" + d, directiveRegex[d]);
                    mapper.append(d);
                }
            }

            var match = temp.match(strayDirective);
            if (match) {
                ParseResult(
                    null,
                    ['"' + match[0] + '" is a bad directivr in format string "' + format + '"']
                )
            }
            else {
                convertedParts.push(temp);
            }
        }
        
        formatRegex = RegExp("^" + convertedParts.join("%") + "$");
        var match = str.match(formatRegex);
        if (match) {
            var len = mapper.length;
            var month = null;
            var year = null;
            for (var i = 0; i < len; i++) {
                switch(mapper[i]) {
                    case 'b':
                        if (month !== null) {
                            ParseResult(
                                null,
                                ['Mutltiple month directives are specified']
                            )
                        }
                        month = abbrMonthToInt(match[i]);
                        break;
                    case 'B':
                        if (month !== null) {
                            ParseResult(
                                null,
                                ['Mutltiple month directives are specified']
                            )
                        }
                        month = monthToInt(match[i]);
                        break;
                    case 'm':
                        if (month !== null) {
                            ParseResult(
                                null,
                                ['Mutltiple month directives are specified']
                            )
                        }
                        month = parseInt(match[i]);
                        break;
                    case 'y':
                        if (year !== null) {
                            ParseResult(
                                null,
                                ['Mutltiple year directives are specified']
                            )
                        }
                        var partialYear = parseInt(match[i]);
                        if (partialYear < 69) {
                            year = partialYear + 2000;
                        }
                        else {
                            year = partialYear + 1900;
                        }
                        break;
                    case 'Y':
                        if (year !== null) {
                            ParseResult(
                                null,
                                ['Mutltiple year directives are specified']
                            )
                        }
                        year = parseInt(match[i]);
                        break;
                }
                var data = match[i];
            }

            if (month !== null && year !== null) {
                return TwoFieldDate(year, month);
            }
            else {
                ParseResult(
                    null,
                    ['both a year and a month must be specified']
                )
            }
        }
        else {
            ParseResult(
                null,
                ['string "' + str + '" does not match format string "' + format + '"']
            )
        }
    }
})();
