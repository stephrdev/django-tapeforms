from django import forms

from tapeforms.contrib.bootstrap import BootstrapTapeformMixin


class DummyForm(BootstrapTapeformMixin, forms.Form):
    my_field1 = forms.CharField()
    my_field2 = forms.BooleanField()


class TestBootstrapTapeformMixin:

    def test_field_template(self):
        form = DummyForm()
        assert form.field_template == 'tapeforms/fields/bootstrap.html'

    def test_field_container_css_class_default(self):
        form = DummyForm()
        assert form.get_field_container_css_class(
            form['my_field1']) == 'form-group'

    def test_field_container_css_class_checkbox(self):
        form = DummyForm()
        assert form.get_field_container_css_class(
            form['my_field2']) == 'form-check'

    def test_field_label_css_class_default(self):
        form = DummyForm()
        assert form.get_field_label_css_class(
            form['my_field1']) is None

    def test_field_label_css_class_checkbox(self):
        form = DummyForm()
        assert form.get_field_label_css_class(
            form['my_field2']) == 'form-check-label'

    def test_widget_css_class_default(self):
        form = DummyForm()
        assert form.get_widget_css_class(
            'my_field1', form.fields['my_field1']) == 'form-control'

    def test_widget_css_class_checkbox(self):
        form = DummyForm()
        assert form.get_widget_css_class(
            'my_field2', form.fields['my_field2']) == 'form-check-input'

    def test_apply_widget_invalid_options(self):
        form = DummyForm({})
        widget = form.fields['my_field1'].widget
        assert 'my_field1' in form.errors
        assert widget.attrs['class'].strip() == 'form-control is-invalid'
