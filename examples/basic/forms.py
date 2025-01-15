from django import forms
from tapeforms.contrib.bootstrap import (
    Bootstrap4TapeformMixin,
    Bootstrap5TapeformMixin,
)
from tapeforms.contrib.foundation import FoundationTapeformMixin
from tapeforms.mixins import TapeformMixin


class SimpleForm(TapeformMixin, forms.Form):
    first_name = forms.CharField(label="First name")
    last_name = forms.CharField(label="Last name", help_text="Some hints")
    confirm = forms.BooleanField(label="Please confirm")


class SimpleWithOverridesForm(TapeformMixin, forms.Form):
    field_template_overrides = {
        forms.CharField: "basic/headline_label_input.html",
        "special_text": "basic/special_widget.html",
    }
    widget_template_overrides = {
        "some_other": "basic/background_input.html",
    }

    some_text = forms.CharField(label="First name")
    some_other = forms.CharField(label="Last name", required=False)
    choose_options = forms.MultipleChoiceField(
        label="Please choose",
        choices=(("foo", "foo"), ("bar", "bar"), ("baz", "bar")),
        widget=forms.RadioSelect,
    )
    special_text = forms.IntegerField(label="A number")


class SimpleBootstrapBaseForm(forms.Form):
    name = forms.CharField(label="Name", help_text="Some hints")
    email = forms.EmailField(label="Email", required=False)
    subject = forms.ChoiceField(
        label="Subject",
        choices=(("option1", "Option 1"), ("option2", "Option 2"), ("option3", "Option 3")),
    )
    message = forms.CharField(label="Message", widget=forms.Textarea(attrs={"rows": "3"}))
    attachment = forms.FileField(label="Attachment", required=False)
    multiple_options = forms.MultipleChoiceField(
        label="Multiple",
        choices=(("option1", "Option 1"), ("option2", "Option 2"), ("option3", "Option 3")),
    )
    choose_options = forms.ChoiceField(
        label="Please choose",
        choices=(("foo", "foo"), ("bar", "bar"), ("baz", "bar")),
        widget=forms.RadioSelect,
    )
    confirm = forms.BooleanField(label="Please confirm")


class SimpleBootstrap4Form(Bootstrap4TapeformMixin, SimpleBootstrapBaseForm):
    pass


class SimpleBootstrap5Form(Bootstrap5TapeformMixin, SimpleBootstrapBaseForm):
    pass


class SimpleFoundationForm(FoundationTapeformMixin, forms.Form):
    first_name = forms.CharField(label="First name")
    last_name = forms.CharField(label="Last name", help_text="Some hints")
    confirm = forms.BooleanField(label="Please confirm")
    choose_options = forms.MultipleChoiceField(
        label="Please choose",
        choices=(("foo", "foo"), ("bar", "bar"), ("baz", "bar")),
        widget=forms.RadioSelect,
    )


class SimpleMultiWidgetForm(TapeformMixin, forms.Form):
    widget_template_overrides = {"birthdate": "basic/select_date_widget.html"}

    birthdate = forms.DateField(widget=forms.SelectDateWidget())
