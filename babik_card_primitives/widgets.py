from django.template.loader import render_to_string
from django.forms.utils import flatatt
from django.forms.widgets import Input, MultiWidget, Select
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class SensitiveInput(Input):
    input_type = 'text'

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if final_attrs.get('client_side_only', False):
            final_attrs.pop('name')
        if value != '':
            final_attrs['value'] = force_text(self._format_value(value))
        return format_html('<input{} />', flatatt(final_attrs))


class SensitiveSelect(Select):
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        if final_attrs.get('client_side_only', False):
            final_attrs.pop('name')
        output = [format_html('<select{}>', flatatt(final_attrs))]
        options = self.render_options([value])
        if options:
            output.append(options)
        output.append('</select>')
        return mark_safe('\n'.join(output))


class TwoFieldCardDateWidget(MultiWidget):
    template = "babik_card_primitives/two_field_card_date_widet.html"

    def decompress(self, value):
        if value:
            return (value.month, value.year)
        else:
            return (None, None)

    def format_output(self, rendered_widgets):
        context = {
            "month_widget": rendered_widgets[0],
            "year_widget": rendered_widgets[1]
        }
        return render_to_string(self.template, context)
