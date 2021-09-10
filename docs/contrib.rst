Contrib
=======

Extra, optional, features of `django-tapeforms`.


Bootstrap mixin
---------------

You can use the :py:class:`tapeforms.contrib.bootstrap.Bootstrap4TapeformMixin`
to render forms with a `Bootstrap 4`_ compatible HTML layout / CSS classes, or
:py:class:`tapeforms.contrib.bootstrap.Bootstrap5TapeformMixin` for `Bootstrap 5`_.

This alternative mixin makes sure that the rendered widgets, fields and labels
have the correct css classes assigned.

In addition, the mixin uses a different template for the fields because Bootstrap
requires that the ordering of label and widget inside a field is swapped (widget
first, label second).

.. _Bootstrap 4: https://getbootstrap.com/docs/4.6/
.. _Bootstrap 5: https://getbootstrap.com/docs/5.0/


Foundation mixin
----------------

You can use the :py:class:`tapeforms.contrib.foundation.FoundationTapeformMixin`
to render forms with a Foundation_ compatible HTML layout / css classes.

This alternative mixin makes sure that the rendered widgets, fields and labels
have the correct CSS classes assigned especially in case of errors.

In addition, the mixin uses a different template for the fields. It is required
to swap the ordering of label and widget when rendering a checkbox, and also to
wrap mulitple inputs - e.g. a group of checkboxes or radio buttons - in a
``fieldset`` element, as `Foundation documentation suggests`__.

.. _Foundation: https://foundation.zurb.com/sites/docs/
.. __: https://foundation.zurb.com/sites/docs/forms.html#checkboxes-and-radio-buttons
