from django import forms

from tapeforms.contrib.foundation import FoundationTapeformMixin


class DummyForm(FoundationTapeformMixin, forms.Form):
    my_field1 = forms.CharField()
    my_field2 = forms.BooleanField()


class DummyFormWithProperties(DummyForm):
    field_label_css_class = 'custom-label'
    widget_css_class = 'some-widget-cssclass'


class TestFoundationTapeformMixin:

    def test_field_template(self):
        form = DummyForm()
        assert form.field_template == 'tapeforms/fields/foundation.html'

    def test_field_label_css_class_default(self):
        form = DummyForm()
        assert form.get_field_label_css_class(
            form['my_field1']) is None

    def test_field_label_css_class_invalid(self):
        form = DummyForm({})
        assert form.get_field_label_css_class(
            form['my_field1']) == 'is-invalid-label'

    def test_field_label_css_class_override_invalid(self):
        form = DummyFormWithProperties({})
        assert form.get_field_label_css_class(
            form['my_field1']) == 'custom-label is-invalid-label'

    def test_add_error(self):
        form = DummyForm({})
        form.add_error(None, 'Non field error!')
        form.add_error('my_field1', 'Error!')
        widget = form.fields['my_field1'].widget
        assert widget.attrs['aria-invalid'] == 'true'
        assert widget.attrs['class'].strip() == 'is-invalid-input'
