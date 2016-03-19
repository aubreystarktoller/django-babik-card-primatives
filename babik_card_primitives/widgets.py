import datetime

from django.template.loader import render_to_string
from django.forms.utils import flatatt
from django.forms.widgets import Input, Widget, Select, MultiWidget
from django.utils.dates import MONTHS
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class SensitiveInput(Input):
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if final_attrs.pop('client_side_only', False):
            final_attrs.pop('name')
        if value != '':
            final_attrs['value'] = force_text(self._format_value(value))
        return format_html('<input{} />', flatatt(final_attrs))


class SensitiveTextInput(SensitiveInput):
    input_type = 'text'


class SensitiveSelect(Select):
    def render(self, name, value, attrs=None, choices=None):
        if choices is None:
            choices = ()
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        if final_attrs.pop('client_side_only', False):
            final_attrs.pop('name')
        output = [format_html('<select{}>', flatatt(final_attrs))]
        options = self.render_options(choices, [value])
        if options:
            output.append(options)
        output.append('</select>')
        return mark_safe('\n'.join(output))


class TwoFieldCardDateWidget(Widget):
    template = "babik_card_primitives/two_field_card_date_widget.html"
    none_value = (0, '---')
    month_field = '%s_month'
    year_field = '%s_year'
    select_widget = SensitiveSelect

    def __init__(self, attrs=None, years=None, months=None, empty_label=None):
        self.attrs = attrs or {}

        # Optional dict of months to use in the "month" select box.
        if months:
            self.months = months
        else:
            self.months = range(1, 13)

        # Optional list or tuple of years to use in the "year" select box.
        if years:
            self.years = years
        else:
            this_year = datetime.date.today().year
            self.years = range(this_year, this_year + 15)

        # Optional string, list, or tuple to use as empty_label.
        if isinstance(empty_label, dict):
            try:
                self.month_none_value = (0, empty_label.pop('month'))
                self.year_none_value = (0, empty_label.pop('year'))
            except KeyError:
                raise ValueError(
                    'empty_label dict must have only "month" and "year" keys.'
                )
            if empty_label:
                raise ValueError(
                    'empty_label dict must have only "month" and "year" keys.'
                )
        else:
            if empty_label is not None:
                self.none_value = (0, empty_label)

            self.year_none_value = self.none_value
            self.month_none_value = self.none_value

    def render(self, name, value, attrs=None):
        if value:
            month_val, year_val = value
        else:
            month_val, year_val = None, None

        ctx = {}
        choices = [(i, i) for i in self.months]
        ctx['month_widget'] = self.create_select(
            name,
            self.month_field,
            value,
            month_val,
            choices,
            self.month_none_value
        )
        choices = [(i, i) for i in self.years]
        ctx['year_widget'] = self.create_select(
            name,
            self.year_field,
            value,
            year_val,
            choices,
            self.year_none_value
        )
        return render_to_string(self.template, ctx)

    def value_from_datadict(self, data, files, name):
        y = data.get(self.year_field % name)
        m = data.get(self.month_field % name)
        if y == m == "0":
            return None
        elif y and m:
            return {'month': m, 'year': y}
        return data.get(name)

    def create_select(self, name, field, value, val, choices, none_value):
        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name
        if not self.is_required:
            choices.insert(0, none_value)
        local_attrs = self.build_attrs(id=field % id_)
        s = self.select_widget(choices=choices)
        select_html = s.render(field % name, val, local_attrs)
        return select_html
