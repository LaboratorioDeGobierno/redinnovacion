from django.forms.utils import flatatt
from django.forms.widgets import CheckboxInput
from django.utils.encoding import force_text
from django.utils.html import format_html


class MtCheckboxInput(CheckboxInput):
    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, type='checkbox', name=name)
        if self.check_test(value):
            final_attrs['checked'] = 'checked'
        if value not in (True, False, None, ''):
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(value)
        template = (
            '<div class="mt-checkbox">'
            '<input{} /><span class="mt-checkbox-span"></span>'
            '</div>'
        )
        return format_html(template, flatatt(final_attrs))
