Changelog
=========

1.1.0 - 2021-09-13
------------------

* Rename Bootstrap mixin to ``Bootstrap4TapeformMixin``, an alias is kept for
  backward compatibility but it will be deprecated and removed at some time
* Remove 'small' CSS class from the help text in Boostrap mixin
* Use 'form-field-' as prefix for container CSS class instead of the value
  returned by ``get_field_container_css_class``
* Add a new ``Bootstrap5TapeformMixin`` mixin for Bootstrap v5
* Add 'form-group' CSS class to checkbox container in Bootstrap mixin


1.0.1 - 2021-04-28
------------------

* Add support for Django 3


1.0.0 - 2021-03-15
------------------

* Add support for Python 3.7 and 3.8
* Remove support for Django 2.0 and 2.1
* Fix duplicated class issue in bootstrap template


0.2.1 - 2019-02-06
------------------

* Change the way extra options are applied to invalid widgets


0.2.0 - 2018-12-12
------------------

* Add support for Foundation flavored forms
* Improve support for applying css classes to invalid fields


0.1.1 - 2018-08-27
------------------

* Fix styling of invalid inputs in Bootstrap forms by adding the correct css class


0.1.0 - 2018-08-17
------------------

* Add ``as_tapeform`` method to Forms to render forms without the need to call
  the ``form`` template tag
* Add hook to update widget options ``apply_widget_options``
* DateInput, TimeInput and SplitDateTimeWidget get a proper input type to
  activate Browser's datepicker.
* Fix invalid help text display if html tags are part of the help text


0.0.4 - 2018-03-22
------------------

* Bugfix release (invalid template path)


0.0.3 - 2018-03-22
------------------

* Improved Bootstrap 4 support


0.0.2 - 2018-03-11
------------------

* Allow ModelForms in `form` template tag.


0.0.1 - 2018-02-27
------------------

* Initial release of `django-tapeforms`
