from .mixins import TapeformLayoutMixin


class TapeformFieldset(TapeformLayoutMixin, object):
    non_field_errors = None

    def __init__(
        self, form, fields=None, exclude=None, primary=False, template=None,
        extra=None
    ):
        assert fields or exclude is not None, 'Please provide fields or exclude argument.'

        self.form = form
        self.render_fields = fields or ()
        self.exclude_fields = exclude or ()
        self.primary_fieldset = primary
        self.extra = extra or {}

        if template:
            self.layout_template = template

    def __repr__(self):
        return '<{cls} form={form}, primary={primary}, fields=({fields})>'.format(
            cls=self.__class__.__name__,
            form=self.form,
            primary=self.primary_fieldset,
            fields=';'.join(self.fields),
        )

    def hidden_fields(self):
        return self.form.hidden_fields() if self.primary_fieldset else ()

    def non_field_errors(self):
        return self.form.non_field_errors() if self.primary_fieldset else ()

    def visible_fields(self):
        form_visible_fields = self.form.visible_fields()

        if self.render_fields:
            fields = self.render_fields
        else:
            fields = [field.name for field in form_visible_fields]

        filtered_fields = [field for field in fields if field not in self.exclude_fields]
        return [field for field in form_visible_fields if field.name in filtered_fields]


class TapeformFieldsetsMixin:
    """
    Mixin to generate fieldsets based on the `fieldsets` property.
    """
    fieldsets = None

    def get_fieldsets(self):
        if not self.fieldsets:
            return []

        has_primary = any(fieldset.get('primary') for fieldset in self.fieldsets)

        for fieldset_config in self.fieldsets:
            kwargs = {'form': self}
            kwargs.update(fieldset_config)

            if not has_primary:
                kwargs['primary'] = True

            fieldset = TapeformFieldset(**kwargs)
            has_primary = True

            yield fieldset
