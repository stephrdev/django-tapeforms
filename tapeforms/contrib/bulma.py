from django.forms import widgets

from ..mixins import TapeformMixin


class BulmaTapeformMixin(TapeformMixin):
    """
    Tapeform Mixin to render Bulma compatible forms.
    (using the template tags provided by `tapeforms`).
    """

    field_template = 'tapeforms/fields/bulma.html'
    field_container_css_class = 'field'
    field_label_css_class = 'label'

    widget_template_overrides = {
        widgets.FileInput: 'tapeforms/widgets/bulma/file.html',
        widgets.ClearableFileInput:
            'tapeforms/widgets/bulma/clearable_file_input.html',
        widgets.RadioSelect: 'tapeforms/widgets/bulma/radio.html',
        widgets.Select: 'tapeforms/widgets/bulma/select.html',
        widgets.SelectMultiple: 'tapeforms/widgets/bulma/select.html',
        widgets.NullBooleanSelect: 'tapeforms/widgets/bulma/select.html',
    }
    widget_css_class = None
    widget_invalid_css_class = 'is-danger'

    def get_field_label_css_class(self, bound_field):
        if isinstance(bound_field.field.widget, widgets.CheckboxInput):
            return 'checkbox'

        return super().get_field_label_css_class(bound_field)

    def get_widget_css_class(self, field_name, field):
        if isinstance(field.widget, widgets.Textarea):
            return 'textarea'

        if isinstance(field.widget, widgets.FileInput):
            return 'file-input'

        if isinstance(field.widget, widgets.Input) and not isinstance(
            field.widget, widgets.CheckboxInput
        ):
            return 'input'

        return super().get_widget_css_class(field_name, field)
