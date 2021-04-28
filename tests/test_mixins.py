from unittest import mock

from django import forms
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.safestring import SafeText

from tapeforms.mixins import TapeformMixin


class DummyForm(TapeformMixin, forms.Form):
    my_hidden = forms.CharField(widget=forms.HiddenInput)
    my_field1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-css'}))
    my_field2 = forms.CharField(help_text='Foo bar<br />baz')
    my_field3 = forms.IntegerField(
        required=False, widget=forms.NumberInput(attrs={'id': 'field3-special'})
    )

    def clean(self):
        if not self.cleaned_data.get('my_field3'):
            raise forms.ValidationError('Non field error!')


class DummyFormWithProperties(DummyForm):
    layout_template = 'some-form-template.html'
    field_template = 'form-wide-field-template.html'
    field_template_overrides = {
        'my_field2': 'field2-template.html',
        forms.IntegerField: 'integer-template.html',
    }
    field_container_css_class = 'form-row-custom'
    field_label_css_class = 'custom-label'
    field_label_invalid_css_class = 'invalid-label'
    widget_template_overrides = {
        'my_field2': 'field2-widget.html',
        forms.NumberInput: 'integer-widget.html',
    }
    widget_css_class = 'some-widget-cssclass'
    widget_invalid_css_class = 'invalid-widget'


class DateTimeDummyForm(TapeformMixin, forms.Form):
    date_field = forms.DateField(widget=forms.DateInput)
    time_field = forms.TimeField(widget=forms.TimeInput)
    split_dt_field = forms.DateTimeField(widget=forms.SplitDateTimeWidget)


class DummyModel(models.Model):
    my_validated_field = models.PositiveIntegerField(
        blank=True, null=True, validators=[MinValueValidator(10)]
    )

    class Meta:
        app_label = 'tapeforms'


class DummyModelForm(TapeformMixin, forms.ModelForm):
    widget_invalid_css_class = 'invalid-widget'

    class Meta:
        model = DummyModel
        fields = '__all__'


class TestRenderMethods:
    @mock.patch('tapeforms.mixins.render_to_string')
    def test_as_tapeform(self, render_mock):
        render_mock.return_value = 'render-mock-called'
        form = DummyForm()
        assert form.as_tapeform() == 'render-mock-called'
        assert render_mock.call_count == 1
        assert render_mock.call_args[0][0] == 'tapeforms/layouts/default.html'
        assert render_mock.call_args[0][1]['form'] == form


class TestLayoutMethods:
    def test_get_layout_template_argument(self):
        assert DummyForm().get_layout_template('form-template.html') == 'form-template.html'

    def test_get_layout_template_property(self):
        assert DummyFormWithProperties().get_layout_template() == ('some-form-template.html')

    def test_get_layout_template_default(self):
        assert DummyForm().get_layout_template() == ('tapeforms/layouts/default.html')

    def test_get_layout_context(self):
        form = DummyForm()
        context = form.get_layout_context()
        assert context['form'] == form
        assert isinstance(context['errors'], forms.utils.ErrorList) is True
        assert len(context['errors']) == 0
        assert len(context['hidden_fields']) == 1
        assert form['my_hidden'] in context['hidden_fields']
        assert len(context['visible_fields']) == 3
        assert form['my_field1'] in context['visible_fields']
        assert form['my_field2'] in context['visible_fields']
        assert form['my_field3'] in context['visible_fields']

    def test_get_layout_context_errors(self):
        form = DummyForm(data={'my_field1': 'foo'})
        context = form.get_layout_context()
        assert len(context['errors']) == 2
        # First non field errors, then hidden field errors.
        assert list(context['errors']) == ['Non field error!', 'This field is required.']


class TestFieldMethods:
    def test_get_field_template_argument(self):
        form = DummyForm()
        assert (
            form.get_field_template(form['my_field2'], 'field-template.html')
            == 'field-template.html'
        )

    def test_get_field_template_name_override(self):
        form = DummyFormWithProperties()
        assert form.get_field_template(form['my_field2']) == 'field2-template.html'

    def test_get_field_template_class_override(self):
        form = DummyFormWithProperties()
        assert form.get_field_template(form['my_field3']) == 'integer-template.html'

    def test_get_field_template_property(self):
        form = DummyFormWithProperties()
        assert form.get_field_template(form['my_field1']) == 'form-wide-field-template.html'

    def test_get_field_template_default(self):
        form = DummyForm()
        assert form.get_field_template(form['my_field1']) == 'tapeforms/fields/default.html'

    def test_get_field_container_css_class_override(self):
        form = DummyFormWithProperties()
        assert form.get_field_container_css_class(form['my_field1']) == 'form-row-custom'

    def test_get_field_container_css_class_default(self):
        form = DummyForm()
        assert form.get_field_container_css_class(form['my_field1']) == 'form-field'

    def test_get_field_label_css_class_override(self):
        form = DummyFormWithProperties()
        assert form.get_field_label_css_class(form['my_field1']) == 'custom-label'

    def test_get_field_label_css_class_invalid(self):
        form = DummyFormWithProperties({})
        assert sorted(form.get_field_label_css_class(form['my_field1']).split(' ')) == [
            'custom-label',
            'invalid-label',
        ]

    def test_get_field_label_css_class_default(self):
        form = DummyForm()
        assert form.get_field_label_css_class(form['my_field1']) is None

    def test_get_field_context(self):
        form = DummyForm()
        context = form.get_field_context(form['my_field1'])
        assert context == {
            'form': form,
            'field': form['my_field1'],
            'field_id': 'id_my_field1',
            'field_name': 'my_field1',
            'errors': [],
            'container_css_class': 'form-field',
            'help_text': None,
            'label': 'My field1',
            'label_css_class': None,
            'required': True,
            'widget_class_name': 'textinput',
            'widget_input_type': 'text',
        }

    def test_get_field_context_custom_id(self):
        form = DummyForm()
        context = form.get_field_context(form['my_field3'])
        assert context == {
            'form': form,
            'field': form['my_field3'],
            'field_id': 'field3-special',
            'field_name': 'my_field3',
            'errors': [],
            'container_css_class': 'form-field',
            'help_text': None,
            'label': 'My field3',
            'label_css_class': None,
            'required': False,
            'widget_class_name': 'numberinput',
            'widget_input_type': 'number',
        }

    def test_get_field_context_no_auto_id(self):
        form = DummyForm(auto_id=False)
        context = form.get_field_context(form['my_field1'])
        assert context['field_id'] == ''

    def test_get_field_context_helptext_is_safe(self):
        form = DummyForm()
        context = form.get_field_context(form['my_field2'])
        assert isinstance(context['help_text'], SafeText) is True
        assert context['help_text'] == 'Foo bar<br />baz'


class TestWidgetMethods:
    def test_apply_widget_options_datetime(self):
        form = DateTimeDummyForm()
        assert form.fields['time_field'].widget.input_type == 'time'
        assert form.fields['date_field'].widget.input_type == 'date'
        assert form.fields['split_dt_field'].widget.widgets[0].input_type == 'date'
        assert form.fields['split_dt_field'].widget.widgets[1].input_type == 'time'

    def test_get_widget_template_name_override(self):
        form = DummyFormWithProperties()
        assert (
            form.get_widget_template('my_field2', form.fields['my_field2'])
            == 'field2-widget.html'
        )

    def test_get_widget_template_class_override(self):
        form = DummyFormWithProperties()
        assert (
            form.get_widget_template('my_field3', form.fields['my_field3'])
            == 'integer-widget.html'
        )

    def test_get_widget_template_default(self):
        form = DummyFormWithProperties()
        assert form.get_widget_template('my_field1', form.fields['my_field1']) is None

    def test_get_widget_css_class_override(self):
        form = DummyFormWithProperties()
        assert (
            form.get_widget_css_class('my_field1', form.fields['my_field1'])
            == 'some-widget-cssclass'
        )

    def test_get_widget_css_class_default(self):
        form = DummyForm()
        assert form.get_widget_css_class('my_field1', form.fields['my_field1']) is None

    def test_apply_widget_invalid_options_css_class(self):
        form = DummyFormWithProperties({})
        assert 'my_field1' in form.errors
        widget = form.fields['my_field1'].widget
        assert sorted(widget.attrs['class'].split(' ')) == [
            'invalid-widget',
            'my-css',
            'some-widget-cssclass',
        ]

    def test_apply_widget_invalid_options_default(self):
        form = DummyForm({})
        assert 'my_field1' in form.errors
        widget = form.fields['my_field1'].widget
        assert widget.attrs['aria-invalid'] == 'true'
        assert widget.attrs['class'] == 'my-css'

    def test_apply_widget_invalid_options_model_validator(self):
        form = DummyModelForm({'my_validated_field': 1})
        assert 'my_validated_field' in form.errors
        widget = form.fields['my_validated_field'].widget
        assert widget.attrs['class'] == 'invalid-widget'
