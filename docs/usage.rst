Usage
=====

Tapeforms provides a :doc:`Mixin <api_mixins>` to add the required functionality to
the Django forms which is required for rendering the whole form and its fields
using Django templates.

.. code-block:: python

    from django import forms
    from tapeforms.mixins import TapeformMixin

    class ContactForm(TapeformMixin, forms.Form):
        name = forms.CharField()
        email = forms.EmailField()
        text = forms.CharField(widget=forms.Textarea)


Together with some template code you get some beautiful rendered forms.

.. code-block:: jinja

    {% load tapeforms %}

    <form method="post" action=".">
        {% csrf_token %}
        {% form form %}
        <button type="submit">Submit</button>
    </form>


By default, the form will be rendered using the ``tapeforms/layouts/default.html``.
To learn how to override the template which is used, please refer to the
:doc:`Advanced usage section <advanced_usage>`.

.. note::

    For a full overview of the methods you might override to customize the rendering
    of your forms, go to the :doc:`API Reference for mixins <api_mixins>`.
