import pytest
from bookkeeper.view.abstract_budget_view import AbstractBudgetView


def test_cannot_create_abstract_repository():
    with pytest.raises(TypeError):
        AbstractBudgetView()


def test_can_create_subclass():
    class Test(AbstractBudgetView):
        def add(self, bgt): pass
        def update(self, bgt): pass
        def handle_exceeding(self, bgts): pass

    t = Test()
    assert isinstance(t, AbstractBudgetView)


def test_set_presenter():
    class Test(AbstractBudgetView):
        def add(self, bgt): pass
        def update(self, bgt): pass
        def handle_exceeding(self, bgts): pass

    class TestPresenter:
        pass

    t = Test()
    p = TestPresenter()
    t.set_presenter(p)
    assert t.bgt_presenter == p
