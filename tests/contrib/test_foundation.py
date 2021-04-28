from django import forms

from tapeforms.contrib.foundation import FoundationTapeformMixin

from . import FormFieldsSnapshotTestMixin


class DummyForm(FoundationTapeformMixin, forms.Form):
    text = forms.CharField()
    checkbox = forms.BooleanField()
    radios = forms.MultipleChoiceField(
        choices=(('foo', 'Foo'), ('bar', 'Bar')), widget=forms.RadioSelect
    )


class DummyFormWithProperties(DummyForm):
    field_label_css_class = 'custom-label'
    widget_css_class = 'some-widget-cssclass'
    field_template = 'form-wide-field-template.html'


class TestFoundationTapeformMixin(FormFieldsSnapshotTestMixin):
    form_class = DummyForm
    snapshot_dir = 'foundation'

    def test_field_template_fieldset(self):
        form = DummyForm()
        assert (
            form.get_field_template(form['radios'])
            == 'tapeforms/fields/foundation_fieldset.html'
        )
        assert (
            form.get_field_template(form['radios'], 'field-template.html')
            == 'field-template.html'
        )
        form = DummyFormWithProperties()
        assert (
            form.get_field_template(form['radios'])
            == 'tapeforms/fields/foundation_fieldset.html'
        )

    def test_apply_widget_invalid_options(self):
        form = DummyForm({})
        assert 'text' in form.errors
        assert form.get_field_label_css_class(form['text']) == 'is-invalid-label'
        widget = form.fields['text'].widget
        assert widget.attrs['class'] == 'is-invalid-input'
