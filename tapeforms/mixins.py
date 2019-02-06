from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from . import defaults
from .utils import join_css_class


class TapeformLayoutMixin:
    """
    Mixin to render a form of fieldset as HTML.
    """

    #: Layout template to use when rendering the form. Optional.
    layout_template = None

    def get_layout_template(self, template_name=None):
        """
        Returns the layout template to use when rendering the form to HTML.

        Preference of template selection:

        1. Provided method argument `template_name`
        2. Form class property `layout_template`
        3. Globally defined default template from `defaults.LAYOUT_DEFAULT_TEMPLATE`

        :param template_name: Optional template to use instead of other configurations.
        :return: Template name to use when rendering the form.
        """
        if template_name:
            return template_name

        if self.layout_template:
            return self.layout_template

        return defaults.LAYOUT_DEFAULT_TEMPLATE

    def get_layout_context(self):
        """
        Returns the context which is used when rendering the form to HTML.

        The generated template context will contain the following variables:

        * form: `Form` instance
        * errors: `ErrorList` instance with non field errors and hidden field errors
        * hidden_fields: All hidden fields to render.
        * visible_fields: All visible fields to render.

        :return: Template context for form rendering.
        """
        errors = self.non_field_errors()
        for field in self.hidden_fields():
            errors.extend(field.errors)

        return {
            'form': self,
            'errors': errors,
            'hidden_fields': self.hidden_fields(),
            'visible_fields': self.visible_fields(),
        }

    def as_tapeform(self):
        """
        Shortcut to render the form as a "tapeform" without including the tapeforms
        templatetags. Behaves similar to `as_p` and `as_table`.
        """
        return render_to_string(
            self.get_layout_template(), self.get_layout_context())


class TapeformMixin(TapeformLayoutMixin):
    """
    Mixin to extend the forms capability to render itself as HTML output.
    (using the template tags provided by `tapeforms`).
    """

    #: Field template to use when rendering a bound form-field. Optional.
    field_template = None

    #: A dictionary of form-field names and/or form-field classes to override
    #: the field template which is used when rendering a certain form-field.
    #: Optional.
    field_template_overrides = None

    #: The CSS class to apply to the form-field container element.
    field_container_css_class = 'form-field'

    #: CSS class to append to the rendered field label tag. Optional.
    field_label_css_class = None

    #: An additional CSS class to append to the rendered field label tag when
    #: the field has errors. Optional.
    field_label_invalid_css_class = None

    #: A dictionary of form-field names and/or widget classes to override
    #: the widget template which is used when rendering a certain form-field.
    #: Optional.
    widget_template_overrides = None

    #: CSS class to append to the widget attributes. Optional.
    widget_css_class = None

    #: An additional CSS class to append to the widget attributes when the field
    #: has errors. Optional.
    widget_invalid_css_class = None

    def __init__(self, *args, **kwargs):
        """
        The init method is overwritten to apply widget templates and CSS classes.
        """
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.apply_widget_options(field_name)
            self.apply_widget_template(field_name)
            self.apply_widget_css_class(field_name)

    def full_clean(self, *args, **kwargs):
        """
        The full_clean method is hijacked to apply special treatment to invalid
        field inputs. For example adding extra options/classes to widgets.
        """
        super().full_clean(*args, **kwargs)
        for field in self.errors:
            if field != NON_FIELD_ERRORS:
                self.apply_widget_invalid_options(field)

    def get_field_template(self, bound_field, template_name=None):
        """
        Returns the field template to use when rendering a form field to HTML.

        Preference of template selection:

        1. Provided method argument `template_name`
        2. Template from `field_template_overrides` selected by field name
        3. Template from `field_template_overrides` selected by field class
        4. Form class property `field_template`
        5. Globally defined default template from `defaults.LAYOUT_FIELD_TEMPLATE`

        :param bound_field: `BoundField` instance to select a template for.
        :param template_name: Optional template to use instead of other configurations.
        :return: Template name to use when rendering the form field.
        """
        if template_name:
            return template_name

        templates = self.field_template_overrides or {}

        template_name = templates.get(bound_field.name, None)
        if template_name:
            return template_name

        template_name = templates.get(bound_field.field.__class__, None)
        if template_name:
            return template_name

        if self.field_template:
            return self.field_template

        return defaults.FIELD_DEFAULT_TEMPLATE

    def get_field_container_css_class(self, bound_field):
        """
        Returns the container CSS class to use when rendering a field template.

        By default, returns the Form class property `field_container_css_class`.

        :param bound_field: `BoundField` instance to return CSS class for.
        :return: A CSS class string.
        """
        return self.field_container_css_class or None

    def get_field_label_css_class(self, bound_field):
        """
        Returns the optional label CSS class to use when rendering a field template.

        By default, returns the Form class property `field_label_css_class`. If the
        field has errors and the Form class property `field_label_invalid_css_class`
        is defined, its value is appended to the CSS class.

        :param bound_field: `BoundField` instance to return CSS class for.
        :return: A CSS class string or `None`
        """
        class_name = self.field_label_css_class

        if bound_field.errors and self.field_label_invalid_css_class:
            class_name = join_css_class(
                class_name, self.field_label_invalid_css_class)

        return class_name or None

    def get_field_context(self, bound_field):
        """
        Returns the context which is used when rendering a form field to HTML.

        The generated template context will contain the following variables:

        * form: `Form` instance
        * field: `BoundField` instance of the field
        * field_id: Field ID to use in `<label for="..">`
        * field_name: Name of the form field to render
        * errors: `ErrorList` instance with errors of the field
        * required: Boolean flag to signal if the field is required or not
        * label: The label text of the field
        * label_css_class: The optional label CSS class, might be `None`
        * help_text: Optional help text for the form field. Might be `None`
        * container_css_class: The CSS class for the field container.
        * widget_class_name: Lowercased version of the widget class name (e.g. 'textinput')
        * widget_input_type: `input_type` property of the widget instance,
          falls back to `widget_class_name` if not available.

        :return: Template context for field rendering.
        """
        widget = bound_field.field.widget
        widget_class_name = widget.__class__.__name__.lower()

        # Check if we have an overwritten id in widget attrs,
        # if not use auto_id of bound field.
        field_id = widget.attrs.get('id') or bound_field.auto_id
        if field_id:
            field_id = widget.id_for_label(field_id)

        return {
            'form': self,
            'field': bound_field,
            'field_id': field_id,
            'field_name': bound_field.name,
            'errors': bound_field.errors,
            'required': bound_field.field.required,
            'label': bound_field.label,
            'label_css_class': self.get_field_label_css_class(bound_field),
            'help_text': mark_safe(bound_field.help_text) if bound_field.help_text else None,
            'container_css_class': self.get_field_container_css_class(bound_field),
            'widget_class_name': widget_class_name,
            'widget_input_type': getattr(widget, 'input_type', None) or widget_class_name
        }

    def apply_widget_options(self, field_name):
        """
        Applies additional widget options like changing the input type of DateInput
        and TimeInput to "date" / "time" to enable Browser date pickers or other
        attributes/properties.
        """
        widget = self.fields[field_name].widget

        if isinstance(widget, forms.DateInput):
            widget.input_type = 'date'

        if isinstance(widget, forms.TimeInput):
            widget.input_type = 'time'

        if isinstance(widget, forms.SplitDateTimeWidget):
            widget.widgets[0].input_type = 'date'
            widget.widgets[1].input_type = 'time'

    def apply_widget_template(self, field_name):
        """
        Applies widget template overrides if available.

        The method uses the `get_widget_template` method to determine if the widget
        template should be exchanged. If a template is available, the template_name
        property of the widget instance is updated.

        :param field_name: A field name of the form.
        """
        field = self.fields[field_name]
        template_name = self.get_widget_template(field_name, field)

        if template_name:
            field.widget.template_name = template_name

    def get_widget_template(self, field_name, field):
        """
        Returns the optional widget template to use when rendering the widget
        for a form field.

        Preference of template selection:
            1. Template from `widget_template_overrides` selected by field name
            2. Template from `widget_template_overrides` selected by widget class

        By default, returns `None` which means "use Django's default widget template".

        :param field_name: The field name to select a widget template for.
        :param field: `Field` instance to return a widget template.
        :return: Template name to use when rendering the widget or `None`
        """
        templates = self.widget_template_overrides or {}

        template_name = templates.get(field_name, None)
        if template_name:
            return template_name

        template_name = templates.get(field.widget.__class__, None)
        if template_name:
            return template_name

        return None

    def apply_widget_css_class(self, field_name):
        """
        Applies CSS classes to widgets if available.

        The method uses the `get_widget_css_class` method to determine if the widget
        CSS class should be changed. If a CSS class is returned, it is appended to
        the current value of the class property of the widget instance.

        :param field_name: A field name of the form.
        """
        field = self.fields[field_name]
        class_name = self.get_widget_css_class(field_name, field)

        if class_name:
            field.widget.attrs['class'] = join_css_class(
                field.widget.attrs.get('class', None), class_name)

    def get_widget_css_class(self, field_name, field):
        """
        Returns the optional widget CSS class to use when rendering the
        form's field widget.

        By default, returns `None` which means "no CSS class / no change".

        :param field_name: The field name of the corresponding field for the widget.
        :param field: `Field` instance to return CSS class for.
        :return: A CSS class string or `None`
        """
        return self.widget_css_class or None

    def apply_widget_invalid_options(self, field_name):
        """
        Applies additional widget options for an invalid field.

        This method is called when there is some error on a field to apply
        additional options on its widget. It does the following:

        * Sets the aria-invalid property of the widget for accessibility.
        * Adds an invalid CSS class, which is determined by the returned value
          of `get_widget_invalid_css_class` method. If a CSS class is returned,
          it is appended to the current value of the class property of the widget.

        :param field_name: A field name of the form.
        """
        field = self.fields[field_name]
        class_name = self.get_widget_invalid_css_class(field_name, field)

        if class_name:
            field.widget.attrs['class'] = join_css_class(
                field.widget.attrs.get('class', None), class_name)

        field.widget.attrs['aria-invalid'] = 'true'

    def get_widget_invalid_css_class(self, field_name, field):
        """
        Returns the optional widget CSS class to append when rendering the
        form's field widget in case of error.

        By default, returns `None` which means "no CSS class / no change".

        :param field_name: The field name of the corresponding field for the widget.
        :param field: `Field` instance to return CSS class for.
        :return: A CSS class string or `None`
        """
        return self.widget_invalid_css_class or None
