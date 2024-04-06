import pytest
from bookkeeper.view.abstract_category_view import AbstractCategoryView


def test_cannot_create_abstract_repository():
    with pytest.raises(TypeError):
        AbstractCategoryView()


def test_can_create_subclass():
    class Test(AbstractCategoryView):
        def add(self, cat): pass
        def update(self, cat): pass
        def delete(self, pk): pass
        def warning(self, msg): pass

    t = Test()
    assert isinstance(t, AbstractCategoryView)


def test_set_presenter():
    class Test(AbstractCategoryView):
        def add(self, cat): pass
        def update(self, cat): pass
        def delete(self, pk): pass
        def warning(self, msg): pass

    class TestPresenter:
        pass

    t = Test()
    p = TestPresenter()
    t.set_presenter(p)
    assert t.cat_presenter == p
