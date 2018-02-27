Installation
============

django-tapeforms supports Python 3 only and requires at least Django 1.11 (because
of the template based widget rendering). No other dependencies are required.

To start, simply install the latest stable package using the command

.. code-block:: shell

    $ pip install django-tapeforms


In addition, you have to add ``'tapeforms'`` to the ``INSTALLED_APP`` setting
in your ``settings.py``.

Thats it, now continue to the :doc:`Usage section <usage>` to learn how to render your
forms to HTML.
