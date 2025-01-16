from django import forms

from ..fieldsets import TapeformFieldset
from ..mixins import TapeformMixin


class BootstrapTapeformFieldset(TapeformFieldset):
    layout_template = "tapeforms/fieldsets/bootstrap.html"


class Bootstrap4TapeformMixin(TapeformMixin):
    """
    Tapeform Mixin to render Bootstrap v4 compatible forms.
    (using the template tags provided by `tapeforms`).
    """

    #: Use a special layout template for Bootstrap compatible forms.
    layout_template = "tapeforms/layouts/bootstrap.html"
    #: Use a special field template for Bootstrap compatible forms.
    field_template = "tapeforms/fields/bootstrap.html"
    #: All form field containers need a CSS class "form-group".
    field_container_css_class = "form-group"
    #: Almost all widgets need a CSS class "form-control".
    widget_css_class = "form-control"
    #: Use a special class to invalid field's widget.
    widget_invalid_css_class = "is-invalid"

    #: Widgets with multiple inputs require some extra care (don't use ul, etc.)
    widget_template_overrides = {
        forms.SelectDateWidget: "tapeforms/widgets/bootstrap_multiwidget.html",
        forms.SplitDateTimeWidget: "tapeforms/widgets/bootstrap_multiwidget.html",
        forms.RadioSelect: "tapeforms/widgets/bootstrap_multipleinput.html",
        forms.CheckboxSelectMultiple: "tapeforms/widgets/bootstrap_multipleinput.html",
    }

    fieldset_class = BootstrapTapeformFieldset

    def get_field_container_css_class(self, bound_field):
        """
        Returns "form-check" if widget is CheckboxInput in addition of the
        default value from the form property ("form-group") - which is returned
        for all other fields.
        """
        class_name = super().get_field_container_css_class(bound_field)

        if isinstance(bound_field.field.widget, forms.CheckboxInput):
            class_name += " form-check"

        return class_name

    def get_field_label_css_class(self, bound_field):
        """
        Returns "form-check-label" if widget is CheckboxInput. For all other fields,
        no CSS class is added.
        """
        if isinstance(bound_field.field.widget, forms.CheckboxInput):
            return "form-check-label"

        return super().get_field_label_css_class(bound_field)

    def get_widget_css_class(self, field_name, field):
        """
        Returns "form-check-input" if input widget is checkable, or
        "form-control-file" if widget is FileInput. For all other fields,
        returns the default value from the form property ("form-control").
        """
        if field.widget.__class__ in [
            forms.RadioSelect,
            forms.CheckboxSelectMultiple,
            forms.CheckboxInput,
        ]:
            return "form-check-input"

        if isinstance(field.widget, forms.FileInput):
            return "form-control-file"

        return super().get_widget_css_class(field_name, field)


class Bootstrap5TapeformMixin(Bootstrap4TapeformMixin):
    """
    Tapeform Mixin to render Bootstrap v5 compatible forms.
    (using the template tags provided by `tapeforms`).
    """

    #: Apply the CSS class "mb-3" to add spacing between the form fields.
    field_container_css_class = "mb-3"
    #: Almost all labels need a CSS class "form-label".
    field_label_css_class = "form-label"

    #: Widgets with multiple inputs require some extra care (don't use ul, etc.)
    widget_template_overrides = {
        forms.SelectDateWidget: "tapeforms/widgets/bootstrap5_multiwidget.html",
        forms.SplitDateTimeWidget: "tapeforms/widgets/bootstrap5_multiwidget.html",
        forms.RadioSelect: "tapeforms/widgets/bootstrap_multipleinput.html",
        forms.CheckboxSelectMultiple: "tapeforms/widgets/bootstrap_multipleinput.html",
    }

    def get_widget_css_class(self, field_name, field):
        """
        Returns "form-check-input" if input widget is checkable, or
        "form-select" if widget is Select or a subclass. For all other fields,
        returns the default value from the form property ("form-control").
        """
        if field.widget.__class__ in [
            forms.RadioSelect,
            forms.CheckboxSelectMultiple,
            forms.CheckboxInput,
        ]:
            return "form-check-input"

        if isinstance(field.widget, forms.Select):
            return "form-select"

        # Don't call super to ensure we bypass the code in the Bootstrap 4 mixin.
        return super(Bootstrap4TapeformMixin, self).get_widget_css_class(field_name, field)
