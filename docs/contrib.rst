Contrib
=======

Extra, optional, features of `django-tapeforms`.


Bootstrap mixin
---------------

You can use the :py:class:`tapeforms.contrib.bootstrap.BootstrapTapeformMixin`
to render forms with a Bootstrap 4 compatible HTML layout / css classes.

This alternative mixin makes sure that the rendered widgets, fields and labels
have the correct css classes assigned.

In addition, the mixin uses a different template for the fields because Bootstrap
requires that the ordering of label and widget inside a field is swapped (widget
first, label second).
