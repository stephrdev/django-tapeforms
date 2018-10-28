Advanced usage
==============

Most of the advanced features are also demo'ed in the examples project you can find
in the `django-tapeforms` codebase. Go to the ``examples`` directory.

.. note::

    Most class properties have a corresponding method to access the value. This
    helps in cases where you might want to manipulate the response in a more
    dynamic way. If you're unsure what can be changed, refer to the
    :doc:`API Reference <api>`.


Overriding layout templates
---------------------------

In the context of `django-tapeforms` the layout template is the outer part of a
form which contains the non field errors and the loop over the fields to render.

If you want to override the template used for rendering the form layout, the best
way is defining a property on the form class:

.. code-block:: python

    class MyForm(TapeformMixin, forms.Form):
        layout_template = 'another-form-template.html'

        field1 = forms.CharField()


You are done. The ``form`` :doc:`template tag <api_templatetags>` will pick the new
defined template for rendering.

If you need to select the layout template on other things like the instance
in ``ModelForm``, you can overwrite the :py:meth:`get_layout_template
<tapeforms.mixins.TapeformLayoutMixin.get_layout_template()>` method.


Overriding field templates
--------------------------

In the context of `django-tapeforms` the field template is the part of a
form which contains the label, widget, errors and help text for a certain field.

If you want to override the template used for rendering fields, there is more
than one way.

When the template should be changed for all fields, you can simply set the
``field_template`` property.

.. code-block:: python

    class MyForm(TapeformMixin, forms.Form):
        field_template = 'my-field-template.html'

        field1 = forms.CharField()


The ``formfield`` :doc:`template tag <api_templatetags>` will now pick the new
defined template for rendering the fields.

You can define the templates used for field rendering in a more specific way.

.. code-block:: python

    class MyForm(TapeformMixin, forms.Form):
        field_template_overrides = {
            'field1': 'my-field1-template.html',
            forms.IntegerField: 'my-number-template.html',
        }

        field1 = forms.CharField()
        field2 = forms.IntegerField()
        field3 = forms.IntegerField()


As you can see, you can override the templates for fields based on the `field name`
and also based on the `field class`.

If you need to select the field template depending on other things, you can
overwrite the :py:meth:`get_field_template
<tapeforms.mixins.TapeformMixin.get_field_template()>` method. It receives a
``BoundField`` instance for the template selection.


Overriding widget templates
---------------------------

In the context of `django-tapeforms` and `Django` itself, the widget template is
used for the actual input element.

If you want to override the template used for rendering widgets, you can change
the ``template_name`` by subclassing the widget classes but this requires much effort.

To make this easier, the `TapeformMixin` provided a helper to set the widget
``template_name``. The matching is done using the field name and widget class.

.. code-block:: python

    class MyForm(TapeformMixin, forms.Form):
        widget_template_overrides = {
            'field1': 'my-field1-widget-template.html',
            forms.NumberInput: 'my-number-widget-template.html',
        }

        field1 = forms.CharField()
        field2 = forms.IntegerField()
        field3 = forms.IntegerField()


If you need to select the widget template based on other things, you can overwrite
the :py:meth:`get_widget_template
<tapeforms.mixins.TapeformMixin.get_widget_template()>` method. It receives the
field name as ``str`` and the ``Field`` instance.


Changing the applied CSS classes
--------------------------------

When you render the form using `django-tapeforms` you can apply CSS classes to
the field container, label and widget.

This is done using the properties ``field_container_css_class``,
``field_label_css_class`` and ``widget_css_class``.

For all CSS class properties, there are methods to override the applied CSS class
per field. Please refer to the :doc:`API Reference <api_mixins>` to learn what
arguments are passed to the CSS class methods.
