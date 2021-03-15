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
    #: Use a special class to invalid field's label.
    field_label_invalid_css_class = 'is-invalid-label'
    #: Use a special class to invalid field's widget.
    widget_invalid_css_class = 'is-invalid-input'

    #: Widgets with multiple inputs require some extra care (don't use ul, etc.)
    widget_template_overrides = {
        forms.RadioSelect: 'tapeforms/widgets/foundation_multipleinput.html',
        forms.CheckboxSelectMultiple: 'tapeforms/widgets/foundation_multipleinput.html'
    }

    def get_field_template(self, bound_field, template_name=None):
        """
        Uses a special field template for widget with multiple inputs. It only
        applies if no other template than the default one has been defined.
        """
        template_name = super().get_field_template(bound_field, template_name)

        if (
            template_name == self.field_template
            and isinstance(
                bound_field.field.widget,
                (forms.RadioSelect, forms.CheckboxSelectMultiple)
            )
        ):
            return 'tapeforms/fields/foundation_fieldset.html'

        return template_name
