Fieldsets
=========

Learn how to organize your form fields in multiple fieldsets and have them rendered nicely.


Manual fieldsets
----------------

The first way to get fieldsets for organizing your form's fields is using the
``TapeformFieldset`` directly. This is also the low-level approach with full
control of whats happening.

.. code-block:: python

    class MyForm(TapeformMixin, forms.Form):
        field1 = forms.CharField()
        field2 = forms.CharField()
        field3 = forms.CharField()
        field4 = forms.CharField(widget=forms.HiddenInput)

        def first_fieldset(self):
            return TapeformFieldset(self, fields=('field1', 'field2'), primary=True)

        def second_fieldset(self):
            return TapeformFieldset(self, exclude=('field1', 'field1'))

.. note::

    You have to make sure that at least one fieldset is marked as your `primary`
    fieldsets. This is required because only the `primary` fieldset will render
    the non field errors and all hidden fields of the form.


The fieldsets can then be rendered using the ``form`` template tag just like classic forms.

.. code-block:: html

    <form action="." method="post" >
        {% csrf_token %}
        <fieldset>
            {% form form.first_fieldset %}
        </fieldset>
        <fieldset>
            {% form form.second_fieldset %}
        </fieldset>
        <button type="submit">Submit</button>
    </form>


Generated fieldsets
-------------------

It might come to your mind that defining alle the fieldsets using methods is a bit to
much boilerplate.

Because of this, django-tapeforms provides another `Mixin` you can use to make
generation of fieldsets a lot easier.

Lets have a look on an example.

.. code-block:: python

    class MyForm(TapeformMixin, forms.Form):
        field1 = forms.CharField()
        field2 = forms.CharField()
        field3 = forms.CharField()
        field4 = forms.CharField(widget=forms.HiddenInput)

        fieldsets = [
            {'fields': ('field1', 'field2')},
            {'exclude': ('field1', 'field2')},  # Render all remaining fields
        ]

Also, the template is simpler now.

.. code-block:: html

    <form action="." method="post" >
        {% csrf_token %}
        {% for fieldset in form.get_fieldsets %}
            <fieldset>
                {% form fieldset %}
            </fieldset>
        {% endfor %}
        <button type="submit">Submit</button>
    </form>


While the difference in code written might not be that big when rendering two fieldsets,
imagine the difference when having lets say 7 oder 8 fieldsets.

As you can see, we don't have to care for the `primary` flag anymore. The ``get_fieldsets``
methods make sure that one fieldset is the primary fieldset (by default, the first fieldset
is marked as `primary`).

There are many methods in the `TapeformFieldsetsMixin` you can override to get your hands
on the generation process (like selection the right fieldset class or manipulating the data
which is used to instantiate the fieldset).

It is also possible to generate the fieldsets configuration on the fly by overriding
the ``get_fieldsets`` method and pass a config to your super call.

.. code-block:: python

    class MyForm(TapeformMixin, forms.Form):
        field1 = forms.CharField()
        field2 = forms.CharField()
        field3 = forms.CharField()
        field4 = forms.CharField(widget=forms.HiddenInput)

        def get_fieldsets(self):
            # Geneate a fieldset for every form field. Why would one do that?
            return super().get_fieldsets([
                {'fields': (field.name,)}
                for field in self.visible_fields()
            ])


Passing around additional data
------------------------------

In more compex setups you might want to pass around additional data. In our example
we assume that we require a css class added to the fieldset element.

.. code-block:: python

    class MyForm(TapeformMixin, forms.Form):
        field1 = forms.CharField()
        field2 = forms.CharField()
        field3 = forms.CharField()
        field4 = forms.CharField(widget=forms.HiddenInput)

        fieldsets = [{
            'fields': ('field1', 'field2'),
            'extra': {'css_class': 'my-class-foo'}
        }, {
            'exclude': ('field1', 'field2'),
            'extra': {'css_class': 'my-class-bar'}
        }]


.. code-block:: html

    <form action="." method="post" >
        {% csrf_token %}
        {% for fieldset in form.get_fieldsets %}
            <fieldset class="{{ fieldset.extra.css_class }}">
                {% form fieldset %}
            </fieldset>
        {% endfor %}
        <button type="submit">Submit</button>
    </form>


The extra key in the fieldset configuration is not checked in any way. Its just passed
around. You might use it to carry things in a ``dic`` like in the example or push
a model instance to the template for further use.


Advanced usage
--------------

For a full overview of the methods TapeformFieldset and TapeformFieldsetsMixin provide,
go to the :doc:`API Reference for fieldsets <api_fieldsets>`.
