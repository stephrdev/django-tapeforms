django-tapeforms
================

.. image:: https://img.shields.io/pypi/v/django-tapeforms.svg
   :target: https://pypi.org/project/django-tapeforms/
   :alt: Latest Version

.. image:: https://github.com/stephrdev/django-tapeforms/workflows/Test/badge.svg?branch=master
   :target: https://github.com/stephrdev/django-tapeforms/actions?workflow=Test
   :alt: CI Status

.. image:: https://codecov.io/gh/stephrdev/django-tapeforms/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/stephrdev/django-tapeforms
   :alt: Coverage Status

.. image:: https://readthedocs.org/projects/django-tapeforms/badge/?version=latest
   :target: https://django-tapeforms.readthedocs.io/en/stable/?badge=latest
   :alt: Documentation Status


Usage
-----

Please refer to the `Documentation <https://django-tapeforms.readthedocs.io/>`_ to
learn how to use ``django-tapeforms``. Basicly, ``tapeforms`` provides a mixin
and some Django template tags to help you render your forms to HTML.


Requirements
------------

django-tapeforms supports Python 3 only and requires at least Django 4.2.
No other dependencies are required.


Prepare for development
-----------------------

The project uses `uv` to manage dependencies and the python environment.

To run the tests, use:

.. code-block:: shell

   $ make tests

To start the example project to experiment with tapeforms, run:

.. code-block:: shell

    $ uv run python examples/manage.py runserver
