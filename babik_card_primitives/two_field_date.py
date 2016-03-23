import re
import datetime
from django.utils.encoding import python_2_unicode_compatible


coversion_specification_re = re.compile(
    "(?P<spec>%(?P<flag>[-_0^#]?)(?P<width>[0-9]*)(?P<type>[bBmyY]))"
)


def _format_to_re(fmt):
    output = [datetime.date(2001, i, 1).strftime(fmt) for i in range(1, 13)]
    return "(?P<%s>%s)" % (fmt[1], "|".join(output))


@python_2_unicode_compatible
class TwoFieldDate(object):
    def __init__(self, year, month):
        try:
            year = int(year)
        except ValueError:
            raise ValueError("year must be an integer")

        self._year = year

        try:
            month = int(month)
        except ValueError:
            raise ValueError("month must be an integer")

        if month < 1 or month > 12:
            raise ValueError("month must be in 1..12")

        self._month = month

    @property
    def year(self):
        return self._year

    @property
    def month(self):
        return self._month

    @staticmethod
    def _get_month(data):
        if "m" in data:
            return int(data['m'])
        elif "b" in data:
            return datetime.datetime.strptime(data['b'], "%b").month
        elif "B" in data:
            return datetime.datetime.strptime(data['B'], "%B").month
        else:
            raise ValueError('month not specified')

    @staticmethod
    def _get_year(data):
        if "Y" in data:
            return int(data["Y"])
        elif "y" in data:
            return datetime.datetime.strptime(data["y"], "%y").year
        else:
            raise ValueError("year not specified")

    @staticmethod
    def _build_re(format):
        _b_months_re = _format_to_re("%b")
        _B_months_re = _format_to_re("%B")

        r = format.replace("%b", _b_months_re, 1)
        r = r.replace("%B", _B_months_re, 1)
        r = r.replace("%m", "(?P<m>[0 ]?[1-9]|1[0-2])", 1)
        r = r.replace("%y", "(?P<y>[0-9]{2})", 1)
        r = r.replace("%Y", "(?P<Y>[0-9]{4})", 1)

        parts = r.split("%%")
        for part in parts:
            match = re.search("%(.)", part)
            if match:
                c = match.group(1)
                if c in "yYbBm":
                    msg = '"%s" directive is repeated format string "%s"'
                else:
                    msg = '"%s" is a bad directive in format string "%s"'
                raise ValueError(msg % (c, format))

        return "^%s$" % "%".join(parts)

    @classmethod
    def parse(cls, date_string, format):
        match = re.match(
            cls._build_re(format),
            date_string,
            flags=re.IGNORECASE
        )
        if match:
            data = match.groupdict()
            return TwoFieldDate(cls._get_year(data), cls._get_month(data))
        else:
            args = (date_string, format)
            raise ValueError(
                'two field date data "%s" does not match format "%s"' % args
            )

    def format(self, fmt_str):
        date = datetime.date(self.year, self.month, 1)

        def replace(match):
            return date.strftime(match.group('spec'))

        def convert(part):
            return coversion_specification_re.sub(replace, part)

        parts = fmt_str.split("%%")
        converted_parts = [convert(p) for p in parts]
        return "%".join(converted_parts)

    def __eq__(self, other):
        return (
            isinstance(other, TwoFieldDate) and
            other.month == self.month and
            other.year == self.year
        )

    def __gt__(self, other):
        if not isinstance(other, TwoFieldDate):
            c = other.__class__
            raise TypeError("unorderable types: TwoFieldDate > %s" % c)
        else:
            return (
                self.year > other.year or
                self.year == other.year and self.month > other.month
            )

    def __ne__(self, other):
        return not (self == other)

    def __ge__(self, other):
        if not isinstance(other, TwoFieldDate):
            c = other.__class__
            raise TypeError("unorderable types: TwoFieldDate >= %s" % c)
        else:
            return self > other or self == other

    def __lt__(self, other):
        if not isinstance(other, TwoFieldDate):
            c = other.__class__
            raise TypeError("unorderable types: TwoFieldDate <= %s" % c)
        else:
            return not (self >= other)

    def __le__(self, other):
        if not isinstance(other, TwoFieldDate):
            c = other.__class__
            raise TypeError("unorderable types: TwoFieldDate < %s" % c)
        else:
            return not (self > other)

    def __hash__(self):
        return hash('%d%02d' % (self.year, self.month))

    def __str__(self):
        return "%s-%s" % (self.year, self.month)
