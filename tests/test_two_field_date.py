import datetime
from django.test import TestCase
from babik_card_primitives.two_field_date import TwoFieldDate

class TwoFieldDateTestCase(TestCase):
    def test_to_large_month(self):
        with self.assertRaises(ValueError):
            TwoFieldDate(2016, 13)

    def test_zero_month(self):
        with self.assertRaises(ValueError):
            TwoFieldDate(2016, 0)

    def test_negative_month(self):
        with self.assertRaises(ValueError):
            TwoFieldDate(2016, -5)

    def test_string_month(self):
        with self.assertRaises(ValueError):
            TwoFieldDate(2016, "a")

    def test_string_year(self):
        with self.assertRaises(ValueError):
            TwoFieldDate("a", 5)

    def test_get_year(self):
        self.assertEqual(TwoFieldDate(2016, 5).year, 2016)

    def test_get_month(self):
        self.assertEqual(TwoFieldDate(2016, 5).month, 5)

    def test_equality(self):
        self.assertEqual(TwoFieldDate(2016, 5), TwoFieldDate(2016, 5))

    def test_inequality_month_mismatch(self):
        self.assertNotEqual(TwoFieldDate(2016, 5), TwoFieldDate(2016, 6))

    def test_inequality_year_mismatch(self):
        self.assertNotEqual(TwoFieldDate(2016, 5), TwoFieldDate(2017, 5))

    def test_inequality_both_mismatch(self):
        self.assertNotEqual(TwoFieldDate(2016, 5), TwoFieldDate(2017, 6))

    def test_inequality_type_mismatch(self):
        self.assertNotEqual(TwoFieldDate(2016, 5), 5)

    def test_greater_wrong_type(self):
        with self.assertRaises(TypeError):
            TwoFieldDate(2016, 5) > 5

    def test_greater_with_year_difference(self):
        self.assertGreater(TwoFieldDate(2016, 5), TwoFieldDate(2015, 5))

    def test_greater_with_month_difference(self):
        self.assertGreater(TwoFieldDate(2016, 5), TwoFieldDate(2016, 4))

    def test_less_wrong_type(self):
        with self.assertRaises(TypeError):
            TwoFieldDate(2016, 5) < 5

    def test_less_with_year_difference(self):
        self.assertLess(TwoFieldDate(2016, 5), TwoFieldDate(2017, 5))

    def test_less_with_month_difference(self):
        self.assertLess(TwoFieldDate(2016, 5), TwoFieldDate(2016, 6))

    def test_less_than_or_equal_with_year_difference(self):
        self.assertLessEqual(TwoFieldDate(2016, 5), TwoFieldDate(2017, 5))

    def test_less_than_or_equal_with_month_difference(self):
        self.assertLessEqual(TwoFieldDate(2016, 5), TwoFieldDate(2016, 6))

    def test_less_than_or_equal_with_same_date(self):
        self.assertLessEqual(TwoFieldDate(2016, 5), TwoFieldDate(2016, 5))

    def test_greater_than_or_equal_with_year_difference(self):
        self.assertGreaterEqual(TwoFieldDate(2017, 5), TwoFieldDate(2016, 5))

    def test_greater_than_or_equal_with_month_difference(self):
        self.assertGreaterEqual(TwoFieldDate(2016, 6), TwoFieldDate(2016, 5))

    def test_greater_than_or_equal_with_same_date(self):
        self.assertGreaterEqual(TwoFieldDate(2016, 5), TwoFieldDate(2016, 5))

    def test_less_or_equal_wrong_type(self):
        with self.assertRaises(TypeError):
            TwoFieldDate(2016, 5) <= 5

    def test_greater_or_equal_wrong_type(self):
        with self.assertRaises(TypeError):
            TwoFieldDate(2016, 5) >= 5

    def test_hash(self):
        self.assertEqual(hash(TwoFieldDate(2016, 5)), hash("201605"))

    def test_format(self):
        self.assertEqual(
            TwoFieldDate(2016, 9).format("%B,%b,%m,%y,%Y,%%"), 
            "September,Sep,09,16,2016,%"
        )

    def test_parse_with_valid_numeric_format(self):
        self.assertEqual(
            TwoFieldDate(2016, 10),
            TwoFieldDate.parse("10-2016", "%m-%Y")
        )

    def test_parse_with_valid_numeric_format_and_liternal_percent(self):
        self.assertEqual(
            TwoFieldDate(2016, 10),
            TwoFieldDate.parse("%-10-2016", "%%-%m-%Y")
        )

    def test_parse_with_valid_numeric_format_and_liternal_percent_next_to_directive(self):
        self.assertEqual(
            TwoFieldDate(2016, 10),
            TwoFieldDate.parse("%10-2016", "%%%m-%Y")
        )

    def test_parse_with_valid_numeric_format_and_short_year(self):
        year = datetime.date.today().year
        y = str(year)[2:]
        self.assertEqual(
            TwoFieldDate(year, 10),
            TwoFieldDate.parse("10-%s" % y, "%m-%y")
        )

    def test_parse_without_month(self):
        with self.assertRaises(ValueError):
            TwoFieldDate.parse("2016", "%Y")

    def test_parse_without_year(self):
        with self.assertRaises(ValueError):
            TwoFieldDate.parse("11", "%m")

    def test_parse_with_zero_padded_numeric_format(self):
        self.assertEqual(
            TwoFieldDate(2016, 1),
            TwoFieldDate.parse("01-2016", "%m-%Y")
        )

    def test_parse_with_space_padded_numeric_format(self):
        self.assertEqual(
            TwoFieldDate(2016, 1),
            TwoFieldDate.parse(" 1-2016", "%m-%Y")
        )

    def test_parse_with_short_month_format(self):
        self.assertEqual(
            TwoFieldDate(2016, 9),
            TwoFieldDate.parse("sep-2016", "%b-%Y")
        )

    def test_parse_with_mixed_case_short_month_format(self):
        self.assertEqual(
            TwoFieldDate(2016, 9),
            TwoFieldDate.parse("sEp-2016", "%b-%Y")
        )

    def test_parse_with_long_month_format(self):
        self.assertEqual(
            TwoFieldDate(2016, 9),
            TwoFieldDate.parse("september-2016", "%B-%Y")
        )

    def test_parse_with_mixed_case_long_month_format(self):
        self.assertEqual(
            TwoFieldDate(2016, 9),
            TwoFieldDate.parse("sePtEmBer-2016", "%B-%Y")
        )

    def test_bad_parse_with_bad_format_string(self):
        with self.assertRaises(ValueError):
            TwoFieldDate.parse("10-2016", "%t")

    def test_bad_parse_with_to_many_valid_tokens(self):
        with self.assertRaises(ValueError):
            TwoFieldDate.parse("10 2016 2016", "%m %Y %Y")

    def test_bad_parse_with_non_matching_strimg(self):
        with self.assertRaises(ValueError):
            TwoFieldDate.parse("10----2016", "%m-%Y")


    def test_string(self):
        self.assertEqual(
            str(TwoFieldDate(2016, 10)),
            "2016-10"
        )
