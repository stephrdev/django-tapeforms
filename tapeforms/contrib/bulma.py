from django.forms import widgets

from ..mixins import TapeformMixin


class BulmaTapeformMixin(TapeformMixin):
    """
    Tapeform Mixin to render Bulma compatible forms.
    (using the template tags provided by `tapeforms`).
    """

    #: Use a special field template for Bulma compatible forms.
    field_template = 'tapeforms/fields/bulma.html'
    #: Bulma requires the "field" class on the field container.
    field_container_css_class = 'field'
    #: Bulma requires the "label" class on the field label.
    field_label_css_class = 'label'

    #: Override some widget templates for Bulma compatible forms.
    widget_template_overrides = {
        widgets.FileInput: 'tapeforms/widgets/bulma/file.html',
        widgets.ClearableFileInput:
            'tapeforms/widgets/bulma/clearable_file_input.html',
        widgets.RadioSelect: 'tapeforms/widgets/bulma/radio.html',
        widgets.Select: 'tapeforms/widgets/bulma/select.html',
        widgets.SelectMultiple: 'tapeforms/widgets/bulma/select.html',
        widgets.NullBooleanSelect: 'tapeforms/widgets/bulma/select.html',
    }
    #: Use a special class to invalid field's widget.
    widget_invalid_css_class = 'is-danger'

    class Media:
        #: Include JavaScript for FileInput widgets.
        js = ('tapeforms/js/bulma_fileinput.js',)

    def get_field_label_css_class(self, bound_field):
        """
        Returns "checkbox" if widget is CheckboxInput. For all other fields,
        return the default value from the form property.
        """
        if isinstance(bound_field.field.widget, widgets.CheckboxInput):
            return 'checkbox'

        return super().get_field_label_css_class(bound_field)

    def get_widget_css_class(self, field_name, field):
        """
        Returns "textarea" if widget is Textarea, "file-input" if it is
        FileInput or "input" if it is based on Input but not CheckboxInput.
        For all other fields, return the default value from the form property.
        """
        if isinstance(field.widget, widgets.Textarea):
            return 'textarea'

        if isinstance(field.widget, widgets.FileInput):
            return 'file-input'

        if isinstance(field.widget, widgets.Input) and not isinstance(
            field.widget, widgets.CheckboxInput
        ):
            return 'input'

        return super().get_widget_css_class(field_name, field)
