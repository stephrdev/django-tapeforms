from django import forms

from ..mixins import TapeformMixin


class FoundationTapeformMixin(TapeformMixin):
    """
    Tapeform Mixin to render Foundation compatible forms.
    (using the template tags provided by `tapeforms`).
    """

    #: Use a special layout template for Foundation compatible forms.
    layout_template = 'tapeforms/layouts/foundation.html'
    #: Use a special field template for Foundation compatible forms.
    field_template = 'tapeforms/fields/foundation.html'
    #: Add a special class to invalid field's label.
    field_label_invalid_css_class = 'is-invalid-label'
    #: Add a special class to invalid field's widget.
    widget_invalid_css_class = 'is-invalid-input'

    #: Widgets with multiple inputs require some extra care (don't use ul, etc.)
    widget_template_overrides = {
        forms.RadioSelect: 'tapeforms/widgets/foundation_multipleinput.html',
        forms.CheckboxSelectMultiple: 'tapeforms/widgets/foundation_multipleinput.html'
    }

    def get_field_label_css_class(self, bound_field):
        """
        Appends 'is-invalid-label' if field has errors.
        """
        class_name = super().get_field_label_css_class(bound_field)

        if bound_field.errors:
            if not class_name:
                class_name = self.field_label_invalid_css_class
            else:
                class_name = '{} {}'.format(
                    class_name, self.field_label_invalid_css_class)

        return class_name

    def get_field_template(self, bound_field, template_name=None):
        """
        Uses a special field template for widget with multiple inputs. It only
        applies if no other template than the default one has been defined.
        """
        template_name = super().get_field_template(bound_field, template_name)

        if (template_name == self.field_template and
                isinstance(bound_field.field.widget, (
                    forms.RadioSelect, forms.CheckboxSelectMultiple))):
            return 'tapeforms/fields/foundation_fieldset.html'

        return template_name

    def add_error(self, field_name, error):
        """
        The method is overwritten to append 'is-invalid-input' to the css class
        of the field's widget.
        """
        super().add_error(field_name, error)

        if field_name in self.fields:
            widget = self.fields[field_name].widget
            widget.attrs['aria-invalid'] = 'true'

            class_names = widget.attrs.get('class', '').split(' ')
            if self.widget_invalid_css_class not in class_names:
                class_names.append(self.widget_invalid_css_class)
                widget.attrs['class'] = ' '.join(class_names)
