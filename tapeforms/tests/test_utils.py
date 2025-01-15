from tapeforms.utils import join_css_class


class TestJoinCssClass:
    def test_output(self):
        assert join_css_class("") == ""
        assert join_css_class("cls1") == "cls1"

    def test_empty(self):
        assert join_css_class("cls1", None) == "cls1"
        assert join_css_class(None, "cls2") == "cls2"

    def test_join_distincts(self):
        assert join_css_class("cls1", "cls1") == "cls1"
        assert sorted(join_css_class("cls1", "cls2", "cls1").split(" ")) == ["cls1", "cls2"]

    def test_join_multiple(self):
        assert sorted(join_css_class("cls1", "cls2 cls3").split(" ")) == [
            "cls1",
            "cls2",
            "cls3",
        ]
        assert sorted(join_css_class("cls1", "cls1 cls2").split(" ")) == ["cls1", "cls2"]
