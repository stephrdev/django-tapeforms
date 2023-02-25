from django import VERSION as django_version
from django import forms

from tapeforms.contrib.bootstrap import (
    Bootstrap4TapeformMixin,
    Bootstrap5TapeformMixin,
    BootstrapTapeformMixin,
)

from . import FormFieldsSnapshotTestMixin


CHOICES = (('foo', 'Foo'), ('bar', 'Bar'))


class DummyBaseForm(forms.Form):
    text = forms.CharField()
    checkbox = forms.BooleanField()
    clearable_file = forms.FileField(required=False)
    radio_select = forms.MultipleChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    splitdatetime = forms.SplitDateTimeField()


class Dummy4Form(Bootstrap4TapeformMixin, DummyBaseForm):
    pass


class Dummy5Form(Bootstrap5TapeformMixin, DummyBaseForm):
    select = forms.ChoiceField(choices=CHOICES)
    select_multiple = forms.MultipleChoiceField(choices=CHOICES)


def test_compatibility_mixin():
    assert BootstrapTapeformMixin == Bootstrap4TapeformMixin


class TestBootstrap4TapeformMixin(FormFieldsSnapshotTestMixin):
    form_class = Dummy4Form
    snapshot_dir = 'bootstrap4' if django_version[0] < 4 else 'bootstrap4_django4'

    def test_apply_widget_invalid_options(self):
        form = self.form_class({})
        assert 'text' in form.errors
        widget = form.fields['text'].widget
        assert sorted(widget.attrs['class'].split(' ')) == ['form-control', 'is-invalid']

    def test_invalid_multiwidget_render(self):
        output = self.render_formfield(self.form_class({})['splitdatetime'])
        self.assertSnapshotMatch(output, 'field_splitdatetime__invalid.html')


class TestBootstrap5TapeformMixin(FormFieldsSnapshotTestMixin):
    form_class = Dummy5Form
    snapshot_dir = 'bootstrap5' if django_version[0] < 4 else 'bootstrap5_django4'

    def test_invalid_multiwidget_render(self):
        output = self.render_formfield(self.form_class({})['splitdatetime'])
        self.assertSnapshotMatch(output, 'field_splitdatetime__invalid.html')
