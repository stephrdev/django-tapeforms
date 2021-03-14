from django import forms

from tapeforms.contrib.bootstrap import BootstrapTapeformMixin

from . import FormFieldsSnapshotTestMixin


class DummyForm(BootstrapTapeformMixin, forms.Form):
    text = forms.CharField()
    checkbox = forms.BooleanField()
    clearable_file = forms.FileField(required=False)
    radio_buttons = forms.MultipleChoiceField(choices=(
        ('foo', 'foo'),
        ('bar', 'bar'),
        ('baz', 'bar')
    ), widget=forms.RadioSelect)


class TestBootstrapTapeformMixin(FormFieldsSnapshotTestMixin):
    form_class = DummyForm
    snapshot_dir = 'bootstrap'

    def test_apply_widget_invalid_options(self):
        form = DummyForm({})
        assert 'text' in form.errors
        widget = form.fields['text'].widget
        assert sorted(widget.attrs['class'].split(' ')) == [
            'form-control', 'is-invalid'
        ]
