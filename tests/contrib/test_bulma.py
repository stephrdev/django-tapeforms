from django import forms

from tapeforms.contrib.bulma import BulmaTapeformMixin

from . import FormFieldsSnapshotTestMixin


class DummyForm(BulmaTapeformMixin, forms.Form):
    CHOICES = (('foo', 'Foo'), ('bar', 'Bar'))

    text = forms.CharField()
    textarea = forms.CharField(widget=forms.Textarea(attrs={'rows': '3'}))
    checkbox = forms.BooleanField(label='Check me')
    radios = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    select = forms.ChoiceField(choices=CHOICES)
    select_multiple = forms.MultipleChoiceField(choices=CHOICES)
    clearable_file = forms.FileField(required=False)


class TestBulmaTapeformMixin(FormFieldsSnapshotTestMixin):
    form_class = DummyForm
    snapshot_dir = 'bulma'

    def test_form_media(self):
        form = DummyForm()
        assert 'tapeforms/js/bulma_fileinput.js"' in str(form.media)
