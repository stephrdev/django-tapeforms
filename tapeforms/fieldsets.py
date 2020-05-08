import copy

from django.forms.utils import ErrorList

from .mixins import TapeformLayoutMixin


class TapeformFieldset(TapeformLayoutMixin, object):
    """
    Class to render a subset of a form's fields. From a template perspective,
    a fieldset looks quite similar to a form (and can use the same template tag
    to render: ``form``.
    """

    def __init__(
        self, form, fields=None, exclude=None, primary=False, template=None,
        extra=None
    ):
        """
        Initializes a fieldset instance to be used like a form in a template.

        Just like in ModelForm Meta, you have to provide at least a list of
        fields to render in this fieldset or a list of fields to exclude.
        If you provide both, exclusions have a higher priority.

        :param form: The form instance to take fields from.
        :param fields: A list of visible field names to include in this fieldset.
        :param exclude: A list of visible fields to _not_ include in this fieldset.
        :param primary: If the fieldset is `primary`, this fieldset is responsible
                        for rendering the hidden fields and non field errors.
        :param template: You can provide an alternative layout template to use.
        :param extra: This argument is carried around with the fieldset and is also
                      available in the template. Useful to pass some special arguments
                      for rendering around (like a fieldset headline.
        :return: A configured fieldset instance.
        """
        assert fields or exclude is not None, 'Please provide fields or exclude argument.'

        self.form = form
        self.render_fields = fields or ()
        self.exclude_fields = exclude or ()
        self.primary_fieldset = primary
        self.extra = extra or {}

        if template:
            self.layout_template = template

    def __repr__(self):
        return '<{cls} form={form}, primary={primary}, fields=({fields})/({exclude})>'.format(
            cls=self.__class__.__name__,
            form=repr(self.form),
            primary=self.primary_fieldset,
            fields=';'.join(self.render_fields),
            exclude=';'.join(self.exclude_fields),
        )

    def hidden_fields(self):
        """
        Returns the hidden fields of the form for rendering of the fieldset is
        marked as the primary fieldset.

        :return: List of bound field instances or empty tuple.
        """
        return self.form.hidden_fields() if self.primary_fieldset else ()

    def non_field_errors(self):
        """
        Returns all non-field errors of the form for rendering of the fieldset is
        marked as the primary fieldset.

        :return: ErrorList instance with non field errors or empty ErrorList.
        """

        return self.form.non_field_errors() if self.primary_fieldset else ErrorList()

    def visible_fields(self):
        """
        Returns the reduced set of visible fields to output from the form.

        This method respects the provided ``fields`` configuration _and_ exlcudes
        all fields from the ``exclude`` configuration.

        If no ``fields`` where provided when configuring this fieldset, all visible
        fields minus the excluded fields will be returned.

        :return: List of bound field instances or empty tuple.
        """

        form_visible_fields = self.form.visible_fields()

        if self.render_fields:
            fields = self.render_fields
        else:
            fields = [field.name for field in form_visible_fields]

        filtered_fields = [field for field in fields if field not in self.exclude_fields]
        return [field for field in form_visible_fields if field.name in filtered_fields]


class TapeformFieldsetsMixin:
    """
    Mixin to generate fieldsets based on the `fieldsets` property of a
    ``TapeformFieldsetsMixin`` enabled form.
    """

    #: Default fieldset class to use when instantiating a fieldset.
    fieldset_class = TapeformFieldset

    #: List/tuple of kwargs as `dict`` to generate fieldsets for.
    fieldsets = None

    def get_fieldset_class(self, **fieldset_kwargs):
        """
        Returns the fieldset class to use when generating the fieldset using
        the passed fieldset kwargs.

        :param fieldset_kwargs: ``dict`` with the fieldset config from ``fieldsets``
        :return: Class to use when instantiating the fieldset.
        """
        return self.fieldset_class

    def get_fieldset(self, **fieldset_kwargs):
        """
        Returns a fieldset instance for the passed ``fieldset_kwargs``.

        :param fieldset_kwargs: ``dict`` with the fieldset config from ``fieldsets``
        :return: Fieldset instance
        """
        cls = self.get_fieldset_class(**fieldset_kwargs)
        return cls(**fieldset_kwargs)

    def get_fieldsets(self, fieldsets=None):
        """
        This method returns a generator which yields fieldset instances.

        The method uses the optional fieldsets argument to generate fieldsets for.
        If no fieldsets argument is passed, the class property ``fieldsets`` is used.

        When generating the fieldsets, the method ensures that at least one fielset
        will be the primary fieldset which is responsible for rendering the non field
        errors and hidden fields.

        :param fieldsets: Alternative set of fieldset kwargs. If passed this set is
                          prevered of the ``fieldsets`` property of the form.
        :return: generator which yields fieldset instances.
        """
        fieldsets = fieldsets or self.fieldsets

        if not fieldsets:
            return

        # Search for primary marker in at least one of the fieldset kwargs.
        has_primary = any(fieldset.get('primary') for fieldset in fieldsets)

        for fieldset_kwargs in fieldsets:
            fieldset_kwargs = copy.deepcopy(fieldset_kwargs)
            fieldset_kwargs['form'] = self

            if not has_primary:
                fieldset_kwargs['primary'] = True
                has_primary = True

            yield self.get_fieldset(**fieldset_kwargs)
