from unittest import mock

import pytest
from django import forms
from django.template import Context, Template, TemplateSyntaxError

from tapeforms.mixins import TapeformMixin


class DummyForm(TapeformMixin, forms.Form):
    my_field1 = forms.CharField()


class TestFormTag:

    @mock.patch('tapeforms.templatetags.tapeforms.render_to_string')
    def test_render(self, render_mock):
        render_mock.return_value = 'render-mock-called'

        form = DummyForm()

        template = Template('{% load tapeforms %}{% form form %}')
        assert template.render(Context({'form': form})) == 'render-mock-called'

        assert render_mock.call_count == 1
        assert render_mock.call_args[0][0] == 'tapeforms/layouts/default.html'
        assert sorted(render_mock.call_args[0][1]) == [
            'errors',
            'form',
            'hidden_fields',
            'visible_fields'
        ]
        assert render_mock.call_args[0][1]['form'] == form

    @mock.patch('tapeforms.templatetags.tapeforms.render_to_string')
    def test_render_using_template(self, render_mock):
        render_mock.return_value = 'render-using-mock-called'

        form = DummyForm()

        template = Template('{% load tapeforms %}{% form form using="foo.html" %}')
        assert template.render(Context({'form': form})) == 'render-using-mock-called'

        assert render_mock.call_count == 1
        assert render_mock.call_args[0][0] == 'foo.html'

    def test_render_invalid_form(self):
        template = Template('{% load tapeforms %}{% form form %}')

        with pytest.raises(TemplateSyntaxError) as exc:
            template.render(Context({'form': object()}))
        assert str(exc.value) == (
            'Provided form should be a `Form` instance, actual type: object')


class TestFormfieldTag:

    @mock.patch('tapeforms.templatetags.tapeforms.render_to_string')
    def test_render(self, render_mock):
        render_mock.return_value = 'render-mock-called'

        form = DummyForm()

        template = Template('{% load tapeforms %}{% formfield form.my_field1 %}')
        assert template.render(Context({'form': form})) == 'render-mock-called'

        assert render_mock.call_count == 1
        assert render_mock.call_args[0][0] == 'tapeforms/fields/default.html'
        assert sorted(render_mock.call_args[0][1]) == [
            'container_css_class',
            'errors',
            'field',
            'field_id',
            'field_name',
            'form',
            'help_html',
            'help_text',
            'label',
            'label_css_class',
            'required',
            'widget_class_name',
            'widget_input_type'
        ]
        assert render_mock.call_args[0][1]['form'] == form
        assert render_mock.call_args[0][1]['field'] == form['my_field1']

    @mock.patch('tapeforms.templatetags.tapeforms.render_to_string')
    def test_render_using_template(self, render_mock):
        render_mock.return_value = 'render-using-mock-called'

        form = DummyForm()

        template = Template(
            '{% load tapeforms %}{% formfield form.my_field1 using="foo.html" %}')
        assert template.render(Context({'form': form})) == 'render-using-mock-called'

        assert render_mock.call_count == 1
        assert render_mock.call_args[0][0] == 'foo.html'

    def test_render_invalid_field(self):
        template = Template('{% load tapeforms %}{% formfield field %}')

        with pytest.raises(TemplateSyntaxError) as exc:
            template.render(Context({'field': object()}))
        assert str(exc.value) == (
            'Provided field should be a `BoundField` instance, actual type: object')
