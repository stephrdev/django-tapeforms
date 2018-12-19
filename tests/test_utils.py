from django.utils.functional import lazystr
from django.utils.safestring import mark_safe

from tapeforms.utils import is_safe, join_css_class


def test_is_safe():
    text = '<h1>title</h1>'
    assert is_safe(text) is False
    assert is_safe(mark_safe(text)) is True
    assert is_safe(lazystr(mark_safe(text))) is True


class TestJoinCssClass:

    def test_output(self):
        assert join_css_class('') == ''
        assert join_css_class('cls1') == 'cls1'

    def test_empty(self):
        assert join_css_class('cls1', None) == 'cls1'
        assert join_css_class(None, 'cls2') == 'cls2'

    def test_join_distincts(self):
        assert join_css_class('cls1', 'cls1') == 'cls1'
        assert sorted(join_css_class('cls1', 'cls2', 'cls1').split(' ')) == [
            'cls1', 'cls2']

    def test_join_multiple(self):
        assert sorted(join_css_class('cls1', 'cls2 cls3').split(' ')) == [
            'cls1', 'cls2', 'cls3']
        assert sorted(join_css_class('cls1', 'cls1 cls2').split(' ')) == [
            'cls1', 'cls2']
