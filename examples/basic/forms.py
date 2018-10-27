from django import forms

from tapeforms.mixins import TapeformMixin
from tapeforms.contrib.bootstrap import BootstrapTapeformMixin
from tapeforms.contrib.foundation import FoundationTapeformMixin


class SimpleForm(TapeformMixin, forms.Form):
    first_name = forms.CharField(label='First name')
    last_name = forms.CharField(label='Last name', help_text='Some hints')
    confirm = forms.BooleanField(label='Please confirm')


class SimpleWithOverridesForm(TapeformMixin, forms.Form):
    field_template_overrides = {
        forms.CharField: 'basic/headline_label_input.html',
        'special_text': 'basic/special_widget.html'
    }
    widget_template_overrides = {
        'some_other': 'basic/background_input.html',
    }

    some_text = forms.CharField(label='First name')
    some_other = forms.CharField(label='Last name', required=False)
    choose_options = forms.MultipleChoiceField(label='Please choose', choices=(
        ('foo', 'foo'),
        ('bar', 'bar'),
        ('baz', 'bar')
    ), widget=forms.RadioSelect)
    special_text = forms.IntegerField(label='A number')


class SimpleBootstrapForm(BootstrapTapeformMixin, forms.Form):
    first_name = forms.CharField(label='First name')
    last_name = forms.CharField(label='Last name', help_text='Some hints')
    confirm = forms.BooleanField(label='Please confirm')


class SimpleFoundationForm(FoundationTapeformMixin, forms.Form):
    first_name = forms.CharField(label='First name')
    last_name = forms.CharField(label='Last name', help_text='Some hints')
    confirm = forms.BooleanField(label='Please confirm')
    choose_options = forms.MultipleChoiceField(label='Please choose', choices=(
        ('foo', 'foo'),
        ('bar', 'bar'),
        ('baz', 'bar')
    ), widget=forms.RadioSelect)


class SimpleMultiWidgetForm(TapeformMixin, forms.Form):
    widget_template_overrides = {
        'birthdate': 'basic/select_date_widget.html'
    }

    birthdate = forms.DateField(widget=forms.SelectDateWidget())
