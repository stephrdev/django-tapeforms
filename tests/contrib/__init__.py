from pathlib import Path

import pytest
from django.template import Context, Template
from django.test.html import parse_html


def prettify_html(element, depth=0):
    """
    Turn an HTML element into a nicely formatted string. It is based on
    `django.test.html.Element.__str__` method and add indentation.
    """
    indent = '  ' * depth
    if isinstance(element, str):
        return '%s%s' % (indent, element)
    output = '%s<%s' % (indent, element.name)
    for key, value in element.attributes:
        if value:
            output += ' %s="%s"' % (key, value)
        else:
            output += ' %s' % key
    output += '>'
    if len(element.children) == 1 and isinstance(element.children[0], str):
        output += '%s</%s>' % (element.children[0], element.name)
    elif element.children:
        depth += 1
        for child in element.children:
            output += '\n%s' % (prettify_html(child, depth))
        output += '\n%s</%s>' % (indent, element.name)
    return output


class FormFieldsSnapshotTestMixin:
    """
    Test mixin to validate the snapshot of each field of `form_class`.
    """

    #: Form class to use when validating fields' snapshots.
    form_class = None

    #: Directory name inside `base_snapshot_dir` where snapshots are stored.
    snapshot_dir = None

    base_snapshot_dir = Path('tests', 'snapshots')

    @pytest.fixture(autouse=True)
    def setupSnapshot(self, snapshot):
        self.snapshot = snapshot
        self.snapshot.snapshot_dir = self.base_snapshot_dir / self.snapshot_dir

    def assertSnapshotMatch(self, output, file_name):
        self.snapshot.assert_match(prettify_html(parse_html(output)), file_name)

    def render_formfield(self, field):
        return Template('{% load tapeforms %}{% formfield field %}').render(
            Context({'field': field})
        )

    def test_form_field_render(self, field_name):
        output = self.render_formfield(self.form_class()[field_name])
        self.assertSnapshotMatch(output, 'field_%s.html' % (field_name))
