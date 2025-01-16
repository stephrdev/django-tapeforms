from django import forms
from tapeforms.contrib.bootstrap import Bootstrap5TapeformMixin
from tapeforms.fieldsets import TapeformFieldset, TapeformFieldsetsMixin
from tapeforms.mixins import TapeformMixin


class LargeForm(TapeformMixin, forms.Form):
    first_name = forms.CharField(label="First name")
    last_name = forms.CharField(label="Last name", help_text="Some hints")
    confirm = forms.BooleanField(label="Please confirm")
    some_text = forms.CharField(label="First name")
    some_other = forms.CharField(label="Last name", required=False)
    choose_options = forms.MultipleChoiceField(
        label="Please choose",
        choices=(("foo", "foo"), ("bar", "bar"), ("baz", "bar")),
        widget=forms.RadioSelect,
    )
    special_text = forms.IntegerField(label="A number")
    birthdate = forms.DateField(widget=forms.SelectDateWidget())


class ManualFieldsetsForm(LargeForm):
    def basic(self):
        return TapeformFieldset(self, fields=("first_name", "last_name"), primary=True)

    def other_stuff(self):
        return TapeformFieldset(self, exclude=("first_name", "last_name"))


class PropertyFieldsetsForm(TapeformFieldsetsMixin, LargeForm):
    fieldsets = (
        {
            "fields": ("first_name", "last_name"),
        },
        {
            "extra": {
                "title": "Other stuff",
                "css_class": "classy",
            },
            "exclude": ("first_name", "last_name"),
        },
    )


class BootstrapFieldsetsForm(Bootstrap5TapeformMixin, TapeformFieldsetsMixin, LargeForm):
    birthdate = forms.DateField()

    fieldsets = (
        {
            "title": "Some fancy title",
            "fields": (("first_name", "last_name"),),
        },
        {
            "exclude": ("first_name", "last_name"),
        },
    )

    def clean(self):
        if not self.cleaned_data.get("first_name") or not self.cleaned_data.get("last_name"):
            self.add_error(None, "Some name fields are missing.")
