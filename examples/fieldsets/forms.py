from django import forms

from tapeforms.fieldsets import TapeformFieldset, TapeformFieldsetsMixin
from tapeforms.mixins import TapeformMixin


class LargeForm(TapeformMixin, forms.Form):
    first_name = forms.CharField(label='First name')
    last_name = forms.CharField(label='Last name', help_text='Some hints')
    confirm = forms.BooleanField(label='Please confirm')
    some_text = forms.CharField(label='First name')
    some_other = forms.CharField(label='Last name', required=False)
    choose_options = forms.MultipleChoiceField(label='Please choose', choices=(
        ('foo', 'foo'),
        ('bar', 'bar'),
        ('baz', 'bar')
    ), widget=forms.RadioSelect)
    special_text = forms.IntegerField(label='A number')
    birthdate = forms.DateField(widget=forms.SelectDateWidget())


class ManualFieldsetsForm(LargeForm):

    def basic(self):
        return TapeformFieldset(
            self, fields=('first_name', 'last_name'), primary=True)

    def other_stuff(self):
        return TapeformFieldset(self, exclude=('first_name', 'last_name'))


class PropertyFieldsetsForm(TapeformFieldsetsMixin, LargeForm):

    fieldsets = ({
        'extra': {
            'title': 'Basic',
        },
        'fields': ('first_name', 'last_name'),
    }, {
        'extra': {
            'title': 'Other stuff',
            'css_class': 'classy',
        },
        'exclude': ('first_name', 'last_name'),
    })
