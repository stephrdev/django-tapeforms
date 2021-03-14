from django import forms

from ..mixins import TapeformMixin


class BootstrapTapeformMixin(TapeformMixin):
    """
    Tapeform Mixin to render Bootstrap4 compatible forms.
    (using the template tags provided by `tapeforms`).
    """

    #: Use a special layout template for Bootstrap compatible forms.
    layout_template = 'tapeforms/layouts/bootstrap.html'
    #: Use a special field template for Bootstrap compatible forms.
    field_template = 'tapeforms/fields/bootstrap.html'
    #: Bootstrap requires that the field has a css class "form-group" applied.
    field_container_css_class = 'form-group'
    #: All widgets need a css class "form-control" (except checkables and file inputs).
    widget_css_class = 'form-control'
    #: Use a special class to invalid field's widget.
    widget_invalid_css_class = 'is-invalid'

    #: Widgets with multiple inputs require some extra care (don't use ul, etc.)
    widget_template_overrides = {
        forms.SelectDateWidget: 'tapeforms/widgets/bootstrap_multiwidget.html',
        forms.SplitDateTimeWidget: 'tapeforms/widgets/bootstrap_multiwidget.html',
        forms.RadioSelect: 'tapeforms/widgets/bootstrap_multipleinput.html',
        forms.CheckboxSelectMultiple: 'tapeforms/widgets/bootstrap_multipleinput.html'
    }

    def get_field_container_css_class(self, bound_field):
        """
        Returns 'form-check' if widget is CheckboxInput. For all other fields,
        return the default value from the form property ("form-group").
        """
        # If we render CheckboxInputs, Bootstrap requires a different
        # container class for checkboxes.
        if isinstance(bound_field.field.widget, forms.CheckboxInput):
            return 'form-check'

        return super().get_field_container_css_class(bound_field)

    def get_field_label_css_class(self, bound_field):
        """
        Returns 'form-check-label' if widget is CheckboxInput. For all other fields,
        no css class is added.
        """
        # If we render CheckboxInputs, Bootstrap requires a different
        # field label css class for checkboxes.
        if isinstance(bound_field.field.widget, forms.CheckboxInput):
            return 'form-check-label'

        return super().get_field_label_css_class(bound_field)

    def get_widget_css_class(self, field_name, field):
        """
        Returns 'form-check-input' if input widget is checkable, or
        'form-control-file' if widget is FileInput. For all other fields
        return the default value from the form property ("form-control").
        """
        # If we render checkable input widget, Bootstrap requires a different
        # widget css class for checkboxes.
        if field.widget.__class__ in [
            forms.RadioSelect,
            forms.CheckboxSelectMultiple,
            forms.CheckboxInput,
        ]:
            return 'form-check-input'

        # Idem for fileinput.
        if isinstance(field.widget, forms.FileInput):
            return 'form-control-file'

        return super().get_widget_css_class(field_name, field)
