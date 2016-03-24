import datetime
from django.test import TestCase
from babik_card_primitives.widgets import (
    SensitiveTextInput,
    SensitiveSelect,
    TwoFieldDateWidget
)

class SensitiveTextInputTestCase(TestCase):
    def test_client_side_only_render_with_none_value(self):
        widget = SensitiveTextInput(attrs={'client_side_only': True})
        output = widget.render('test', None)
        self.assertHTMLEqual(output, '<input type="text" />')

    def test_client_side_only_render_with_no_value(self):
        widget = SensitiveTextInput(attrs={'client_side_only': True})
        output = widget.render('test', '')
        self.assertHTMLEqual(output, '<input type="text" />')

    def test_client_side_only_render_with_value(self):
        widget = SensitiveTextInput(attrs={'client_side_only': True})
        output = widget.render('test', 'test value')
        self.assertHTMLEqual(output, '<input type="text" value="test value" />')

    def test_client_side_only_render_with_extra_attrs(self):
        widget = SensitiveTextInput(attrs={'client_side_only': True})
        output = widget.render('test', 'test value', attrs = {'extra': 'extra'} )
        self.assertHTMLEqual(output, '<input type="text" value="test value" extra="extra" />')

    def test_render_with_none_value(self):
        widget = SensitiveTextInput()
        output = widget.render('test', None)
        self.assertHTMLEqual(output, '<input type="text" name="test" />')

    def test_render_with_no_value(self):
        widget = SensitiveTextInput()
        output = widget.render('test', '')
        self.assertHTMLEqual(output, '<input type="text" name="test" />')

    def test_render_with_value(self):
        widget = SensitiveTextInput()
        output = widget.render('test', 'test value')
        self.assertHTMLEqual(output, '<input type="text" value="test value" name="test" />')

    def test_render_with_extra_attrs(self):
        widget = SensitiveTextInput()
        output = widget.render('test', 'test value', attrs = {'extra': 'extra'} )
        self.assertHTMLEqual(output, '<input type="text" value="test value" extra="extra" name="test" />')


class SensitiveSelectTestCase(TestCase):
    CHOICES = (
        ('test', 'test'),
    )

    def test_render_with_none_value(self):
        widget = SensitiveSelect(choices = self.CHOICES)
        output = widget.render('test', None)
        self.assertHTMLEqual(
            output,
            '<select name="test"><option value="test">test</option></select>'
        )

    def test_render_with_empty_value(self):
        widget = SensitiveSelect(choices = self.CHOICES)
        output = widget.render('test', '')
        self.assertHTMLEqual(
            output,
            '<select name="test"><option value="test">test</option></select>'
        )

    def test_render_with_bad_value(self):
        widget = SensitiveSelect(choices = self.CHOICES)
        output = widget.render('test', 'test1')
        self.assertHTMLEqual(
            output,
            '<select name="test"><option value="test">test</option></select>'
        )

    def test_render_with_value(self):
        widget = SensitiveSelect(choices = self.CHOICES)
        output = widget.render('test', 'test')
        self.assertHTMLEqual(
            output,
            '<select name="test"><option selected="selected" value="test">test</option></select>'
        )

    def test_client_side_only_render_with_none_value(self):
        widget = SensitiveSelect(choices = self.CHOICES, attrs={'client_side_only':True})
        output = widget.render('test', None)
        self.assertHTMLEqual(
            output,
            '<select><option value="test">test</option></select>'
        )

    def test_client_side_only_render_with_empty_value(self):
        widget = SensitiveSelect(choices = self.CHOICES, attrs={'client_side_only':True})
        output = widget.render('test', '')
        self.assertHTMLEqual(
            output,
            '<select><option value="test">test</option></select>'
        )

    def test_client_side_only_render_with_bad_value(self):
        widget = SensitiveSelect(choices = self.CHOICES, attrs={'client_side_only':True})
        output = widget.render('test', 'test1')
        self.assertHTMLEqual(
            output,
            '<select><option value="test">test</option></select>'
        )

    def test_client_side_only_render_with_value(self):
        widget = SensitiveSelect(choices = self.CHOICES, attrs={'client_side_only':True})
        output = widget.render('test', 'test')
        self.assertHTMLEqual(
            output,
            '<select><option selected="selected" value="test">test</option></select>'
        )

    def test_render_with_extra_choices(self):
        widget = SensitiveSelect(choices = self.CHOICES)
        output = widget.render('test', None, choices=(('test1', 'test1'),))
        self.assertHTMLEqual(
            output,
            '<select name="test"><option value="test">test</option><option value="test1">test1</option></select>'
        )

    def test_render_with_no_choices(self):
        widget = SensitiveSelect()
        output = widget.render('test', None)
        self.assertHTMLEqual(
            output,
            '<select name="test"></select>'
        )

    def test_client_side_only_render_with_no_choices(self):
        widget = SensitiveSelect(attrs={'client_side_only': True})
        output = widget.render('test', None)
        self.assertHTMLEqual(
            output,
            '<select></select>'
        )


class TwoFieldDateWidgetTestCase(TestCase):
    maxDiff = None

    def _build_options(self, cs, selected=None):
        options = []
        for c in cs:
            label, value = c
            if label == selected:
                options.append(
                    """
                    <option selected="selected" value="{label}">
                        {value}
                    </option>
                    """.format(label=label, value=value)
                )
            else:
                options.append(
                    """
                    <option value="{label}">
                        {value}
                    </option>
                    """.format(label=label, value=value)
                )
        return ''.join(options) 

    def test_render_with_default_options(self):
        widget = TwoFieldDateWidget()
        output = widget.render("test", None)

        month_choices = [(n, n) for n in range(1,13)]
        months = self._build_options([(0, '---')] + month_choices)
        this_year = datetime.date.today().year
        year_choices = [(n, n) for n in range(this_year,this_year+15)]
        years = self._build_options([(0, '---')] + year_choices)
        self.assertHTMLEqual(
            output,
            """
            <span class="babik-card-primitives-month-field">
            <select id="id_test_month" name="test_month">
            {months}
            </select>
            </span>
            <span class="babik-card-primitives-year-field">
            <select id="id_test_year" name="test_year">
            {years}
            </select>
            </span>
            """.format(months=months, years=years)
        )

    def test_render_with_single_empty_value(self):
        widget = TwoFieldDateWidget(empty_label = 'test')
        output = widget.render("test", None)

        month_choices = [(n, n) for n in range(1,13)]
        months = self._build_options([(0, 'test')] + month_choices)
        this_year = datetime.date.today().year
        year_choices = [(n, n) for n in range(this_year,this_year+15)]
        years = self._build_options([(0, 'test')] + year_choices)
        self.assertHTMLEqual(
            output,
            """
            <span class="babik-card-primitives-month-field">
            <select id="id_test_month" name="test_month">
            {months}
            </select>
            </span>
            <span class="babik-card-primitives-year-field">
            <select id="id_test_year" name="test_year">
            {years}
            </select>
            </span>
            """.format(months=months, years=years)
        )

    def test_render_with_dict_empty_value(self):
        widget = TwoFieldDateWidget(
            empty_label = {'month':'test_month', 'year':'test_year'}
        )
        output = widget.render("test", None)

        month_choices = [(n, n) for n in range(1,13)]
        months = self._build_options([(0, 'test_month')] + month_choices)
        this_year = datetime.date.today().year
        year_choices = [(n, n) for n in range(this_year,this_year+15)]
        years = self._build_options([(0, 'test_year')] + year_choices)
        self.assertHTMLEqual(
            output,
            """
            <span class="babik-card-primitives-month-field">
            <select id="id_test_month" name="test_month">
            {months}
            </select>
            </span>
            <span class="babik-card-primitives-year-field">
            <select id="id_test_year" name="test_year">
            {years}
            </select>
            </span>
            """.format(months=months, years=years)
        )

    def test_invalid_empty_value_with_missing_key(self):
        with self.assertRaises(ValueError):
            widget = TwoFieldDateWidget(empty_label = {"month": 'x'})

    def test_invalid_empty_value_with_unknown_key(self):
        with self.assertRaises(ValueError):
            widget = TwoFieldDateWidget(
                empty_label = {
                    "month": "test_month",
                    "year": "test_year",
                    "extra": "extra"
                }
            )

    def test_render_with_set_months(self):
        widget = TwoFieldDateWidget(months = (1, 2))
        output = widget.render("test", None)

        month_choices = [(n, n) for n in (1, 2)]
        months = self._build_options([(0, '---')] + month_choices)
        this_year = datetime.date.today().year
        year_choices = [(n, n) for n in range(this_year,this_year+15)]
        years = self._build_options([(0, '---')] + year_choices)
        self.assertHTMLEqual(
            output,
            """
            <span class="babik-card-primitives-month-field">
            <select id="id_test_month" name="test_month">
            {months}
            </select>
            </span>
            <span class="babik-card-primitives-year-field">
            <select id="id_test_year" name="test_year">
            {years}
            </select>
            </span>
            """.format(months=months, years=years)
        )

    def test_render_with_set_years(self):
        widget = TwoFieldDateWidget(years = (2016, 2017))
        output = widget.render("test", None)

        month_choices = [(n, n) for n in range(1,13)]
        months = self._build_options([(0, '---')] + month_choices)
        year_choices = [(n, n) for n in (2016, 2017)]
        years = self._build_options([(0, '---')] + year_choices)
        self.assertHTMLEqual(
            output,
            """
            <span class="babik-card-primitives-month-field">
            <select id="id_test_month" name="test_month">
            {months}
            </select>
            </span>
            <span class="babik-card-primitives-year-field">
            <select id="id_test_year" name="test_year">
            {years}
            </select>
            </span>
            """.format(months=months, years=years)
        )

    def test_render_with_non_empty_value(self):
        this_year = datetime.date.today().year
        widget = TwoFieldDateWidget()
        output = widget.render("test", (1, this_year))

        month_choices = [(n, n) for n in range(1,13)]
        months = self._build_options([(0, '---')] + month_choices, 1)
        year_choices = [(n, n) for n in range(this_year,this_year+15)]
        years = self._build_options([(0, '---')] + year_choices, this_year)
        self.assertHTMLEqual(
            output,
            """
            <span class="babik-card-primitives-month-field">
            <select id="id_test_month" name="test_month">
            {months}
            </select>
            </span>
            <span class="babik-card-primitives-year-field">
            <select id="id_test_year" name="test_year">
            {years}
            </select>
            </span>
            """.format(months=months, years=years)
        )

    def test_render_with_is_required(self):
        this_year = datetime.date.today().year
        widget = TwoFieldDateWidget()
        widget.is_required = True
        output = widget.render("test", None)

        month_choices = [(n, n) for n in range(1,13)]
        months = self._build_options(month_choices)
        year_choices = [(n, n) for n in range(this_year,this_year+15)]
        years = self._build_options(year_choices)
        self.assertHTMLEqual(
            output,
            """
            <span class="babik-card-primitives-month-field">
            <select id="id_test_month" name="test_month">
            {months}
            </select>
            </span>
            <span class="babik-card-primitives-year-field">
            <select id="id_test_year" name="test_year">
            {years}
            </select>
            </span>
            """.format(months=months, years=years)
        )

    def test_render_with_id(self):
        this_year = datetime.date.today().year
        widget = TwoFieldDateWidget(attrs={'id':'myid'})
        widget.is_required = True
        output = widget.render("test", None)

        month_choices = [(n, n) for n in range(1,13)]
        months = self._build_options(month_choices)
        year_choices = [(n, n) for n in range(this_year,this_year+15)]
        years = self._build_options(year_choices)
        self.assertHTMLEqual(
            output,
            """
            <span class="babik-card-primitives-month-field">
            <select id="myid_month" name="test_month">
            {months}
            </select>
            </span>
            <span class="babik-card-primitives-year-field">
            <select id="myid_year" name="test_year">
            {years}
            </select>
            </span>
            """.format(months=months, years=years)
        )

    def test_value_from_datadict_with_zero_value(self):
        widget = TwoFieldDateWidget()
        d = widget.value_from_datadict(
            {'test_month': "0", 'test_year': "0"},
            [],
            'test'
        )
        self.assertEqual(d, None)

    def test_value_from_datadict_with_set_value(self):
        widget = TwoFieldDateWidget()
        d = widget.value_from_datadict(
            {'test_month': "1", 'test_year': "2016"},
            [],
            'test'
        )
        self.assertEqual(d, {"month": "1", "year": "2016"})

    def test_value_from_datadict_with_partial_value(self):
        widget = TwoFieldDateWidget()
        d = widget.value_from_datadict({'test_month': 'x'}, [], 'test')
        self.assertEqual(d, None)

    def test_render_with_client_side_only(self):
        widget = TwoFieldDateWidget(attrs={"client_side_only":True})
        output = widget.render("test", None)

        month_choices = [(n, n) for n in range(1,13)]
        months = self._build_options([(0, '---')] + month_choices)
        this_year = datetime.date.today().year
        year_choices = [(n, n) for n in range(this_year,this_year+15)]
        years = self._build_options([(0, '---')] + year_choices)
        self.assertHTMLEqual(
            output,
            """
            <span class="babik-card-primitives-month-field">
            <select id="id_test_month">
            {months}
            </select>
            </span>
            <span class="babik-card-primitives-year-field">
            <select id="id_test_year">
            {years}
            </select>
            </span>
            """.format(months=months, years=years)
        )
