import pytest
from bookkeeper.view.abstract_expense_view import AbstractExpenseView


def test_cannot_create_abstract_repository():
    with pytest.raises(TypeError):
        AbstractExpenseView()


def test_can_create_subclass():
    class Test(AbstractExpenseView):
        def add(self, exp, cat_name): pass
        def update(self, exp, cat_name): pass
        def delete(self, pk): pass
        def add_category(self, cat): pass
        def update_category(self, cat): pass
        def delete_category(self, pk): pass

    t = Test()
    assert isinstance(t, AbstractExpenseView)


def test_set_presenter():
    class Test(AbstractExpenseView):
        def add(self, exp, cat_name): pass
        def update(self, exp, cat_name): pass
        def delete(self, pk): pass
        def add_category(self, cat): pass
        def update_category(self, cat): pass
        def delete_category(self, pk): pass

    class TestPresenter:
        pass

    t = Test()
    p = TestPresenter()
    t.set_presenter(p)
    assert t.exp_presenter == p
