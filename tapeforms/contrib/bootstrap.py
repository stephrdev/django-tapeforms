from django import forms

from ..mixins import TapeformMixin


class BootstrapTapeformMixin(TapeformMixin):
    """
    Tapeform Mixin to render Bootstrap4 compatible forms.
    (using the template tags provided by `tapeforms`).
    """

    field_template = 'tapeforms/fields/bootstrap.html'
    field_container_css_class = 'form-group'
    widget_css_class = 'form-control'

    def get_field_container_css_class(self, bound_field):
        """
        Returns 'form-check' if widget is CheckboxInput.
        """
        # If we render CheckboxInputs, Bootstrap requires a different
        # container class for checkboxes.
        if isinstance(bound_field.field.widget, forms.CheckboxInput):
            return 'form-check'

        return super().get_field_container_css_class(bound_field)

    def get_field_label_css_class(self, bound_field):
        """
        Returns 'form-check-label' if widget is CheckboxInput.
        """
        # If we render CheckboxInputs, Bootstrap requires a different
        # field label css class for checkboxes.
        if isinstance(bound_field.field.widget, forms.CheckboxInput):
            return 'form-check-label'

        return super().get_field_label_css_class(bound_field)

    def get_widget_css_class(self, field_name, field):
        """
        Returns 'form-check-input' if widget is CheckboxInput.
        """
        # If we render CheckboxInputs, Bootstrap requires a different
        # widget css class for checkboxes.
        if isinstance(field.widget, forms.CheckboxInput):
            return 'form-check-input'

        return super().get_widget_css_class(field_name, field)
