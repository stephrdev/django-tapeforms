from . import FormFieldsSnapshotTestMixin


def pytest_generate_tests(metafunc):
    # Set the field_name parametrization for the form class defined in
    # FormFieldsSnapshotTestMixin derived class
    if metafunc.cls and issubclass(metafunc.cls, FormFieldsSnapshotTestMixin):
        if "field_name" in metafunc.fixturenames:
            try:
                fields = metafunc.cls.form_class.declared_fields.keys()
            except AttributeError:
                raise ValueError(f"{metafunc.cls!r} must define a valid form_class property")
            metafunc.parametrize("field_name", fields)
