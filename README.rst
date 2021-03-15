django-tapeforms
================

.. image:: https://img.shields.io/pypi/v/django-tapeforms.svg
   :target: https://pypi.python.org/pypi/django-tapeforms
   :alt: Latest Version

.. image:: https://codecov.io/gh/stephrdev/django-tapeforms/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/stephrdev/django-tapeforms
   :alt: Coverage Status

.. image:: https://readthedocs.org/projects/django-tapeforms/badge/?version=latest
   :target: https://django-tapeforms.readthedocs.io/en/stable/?badge=latest
   :alt: Documentation Status

.. image:: https://travis-ci.org/stephrdev/django-tapeforms.svg?branch=master
   :target: https://travis-ci.org/stephrdev/django-tapeforms

Usage
-----

Please refer to the `Documentation <https://django-tapeforms.readthedocs.io/>`_ to
learn how to use ``django-tapeforms``. Basicly, ``tapeforms`` provides a mixin
and some Django template tags to help you render your forms to HTML.


Requirements
------------

django-tapeforms supports Python 3 only and requires at least Django 1.11 (because
of the template based widget rendering). No other dependencies are required.


Prepare for development
-----------------------

A Python 3.6 interpreter is required in addition to pipenv.

.. code-block:: shell

    $ pipenv install --dev
    $ pipenv run pip install -e .


Now you're ready to start the example project to experiment with tapeforms.

.. code-block:: shell

    $ pipenv run python examples/manage.py runserver
