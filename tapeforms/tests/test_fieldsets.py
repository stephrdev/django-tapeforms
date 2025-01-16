import pytest
from django import forms

from tapeforms.fieldsets import TapeformFieldset, TapeformFieldsetsMixin
from tapeforms.mixins import TapeformMixin


class DummyForm(TapeformMixin, forms.Form):
    my_field1 = forms.CharField()
    my_field2 = forms.CharField()
    my_field3 = forms.CharField(widget=forms.HiddenInput)
    my_field4 = forms.CharField()

    def clean(self):
        if not self.cleaned_data.get("my_field2"):
            raise forms.ValidationError("Non field error!")


class DummyFormWithEmptyFieldsets(TapeformFieldsetsMixin, DummyForm):
    pass


class DummyFormWithFieldsets(TapeformFieldsetsMixin, DummyForm):
    fieldsets = [
        {"fields": ("my_field1",)},
        {"exclude": ("my_field1",)},
    ]


class DummyFormWithAdvancedFieldsets(TapeformFieldsetsMixin, DummyForm):
    fieldsets = [
        {"fields": ("my_field1",)},
        {"exclude": ("my_field1",), "primary": True},
    ]


class TestTapeformFieldset:
    def test_init(self):
        form = DummyForm()
        fieldset = TapeformFieldset(form, fields=("my_field1",))
        assert fieldset.form == form
        assert fieldset.render_fields == ("my_field1",)
        assert fieldset.layout_template == "tapeforms/fieldsets/default.html"

    def test_init_with_template(self):
        form = DummyForm()
        fieldset = TapeformFieldset(form, fields=("my_field1",), template="fieldset.html")
        assert fieldset.layout_template == "fieldset.html"

    def test_repr(self):
        form = DummyForm()
        fieldset = TapeformFieldset(form, exclude=("my_field3",))
        assert repr(fieldset) == (
            "<TapeformFieldset form=<DummyForm bound=False, valid=Unknown, "
            "fields=(my_field1;my_field2;my_field3;my_field4)>, primary=False, "
            "title=None, fields=()/(my_field3)>"
        )

    def test_hidden_fields_primary(self):
        form = DummyForm()
        fieldset = TapeformFieldset(form, fields=("my_field1",), primary=True)
        assert len(fieldset.hidden_fields()) == 1

    def test_hidden_fields_not_primary(self):
        form = DummyForm()
        fieldset = TapeformFieldset(form, fields=("my_field1",), primary=False)
        assert len(fieldset.hidden_fields()) == 0
        assert isinstance(fieldset.hidden_fields(), tuple) is True

    def test_non_field_errors_primary(self):
        form = DummyForm(data={})
        fieldset = TapeformFieldset(form, fields=("my_field1",), primary=True)
        assert len(fieldset.non_field_errors()) == 1

    def test_non_field_errors_not_primary(self):
        form = DummyForm(data={})
        fieldset = TapeformFieldset(form, fields=("my_field1",), primary=False)
        assert len(fieldset.non_field_errors()) == 0
        assert isinstance(fieldset.non_field_errors(), forms.utils.ErrorList) is True

    def test_visible_fields_with_fields(self):
        form = DummyForm()
        fieldset = TapeformFieldset(form, fields=("my_field1",))
        assert [f.name for f in fieldset.visible_fields()[0]] == ["my_field1"]

    def test_visible_fields_with_fields_and_exclude(self):
        form = DummyForm()
        fieldset = TapeformFieldset(
            form, fields=("my_field1", "my_field2"), exclude=("my_field2",)
        )
        assert [f.name for f in fieldset.visible_fields()[0]] == ["my_field1"]

    def test_visible_fields_with_exclude(self):
        form = DummyForm()
        fieldset = TapeformFieldset(form, exclude=("my_field1",))
        assert [f.name for f in fieldset.visible_fields()[0]] == ["my_field2"]
        assert [f.name for f in fieldset.visible_fields()[1]] == ["my_field4"]

    def test_visible_fields_with_columns(self):
        form = DummyForm()
        fieldset = TapeformFieldset(form, fields=("my_field1", ("my_field2", "my_field4")))
        assert [f.name for f in fieldset.visible_fields()[0]] == ["my_field1"]
        assert [f.name for f in fieldset.visible_fields()[1]] == ["my_field2", "my_field4"]


class TestTapeformFieldsetsMixin:
    def test_get_fieldset_class(self):
        form = DummyFormWithFieldsets()
        assert form.get_fieldset_class() == TapeformFieldset

    def test_get_fieldset(self):
        form = DummyFormWithFieldsets()
        fieldset = form.get_fieldset(form=form, fields=("my_field1",))
        assert isinstance(fieldset, TapeformFieldset)
        assert fieldset.form == form
        assert fieldset.render_fields == ("my_field1",)

    def test_get_fieldsets_empty(self):
        form = DummyFormWithEmptyFieldsets()
        fieldsets = list(form.get_fieldsets())
        assert len(fieldsets) == 1
        assert fieldsets[0].primary_fieldset is True
        assert [row[0].name for row in fieldsets[0].visible_fields()] == [
            'my_field1', 'my_field2', 'my_field4']

    def test_get_fieldsets_auto_primary(self):
        form = DummyFormWithFieldsets()
        fieldsets = list(form.get_fieldsets())
        assert len(fieldsets) == 2
        assert fieldsets[0].primary_fieldset is True
        assert fieldsets[1].primary_fieldset is False

    def test_get_fieldsets_explicit_primary(self):
        form = DummyFormWithAdvancedFieldsets()
        fieldsets = list(form.get_fieldsets())
        assert len(fieldsets) == 2
        assert fieldsets[0].primary_fieldset is False
        assert fieldsets[1].primary_fieldset is True
