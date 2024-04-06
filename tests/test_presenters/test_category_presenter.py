import pytest
from datetime import datetime, timedelta
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.view.abstract_budget_view import AbstractBudgetView
from bookkeeper.view.abstract_expense_view import AbstractExpenseView
from bookkeeper.view.abstract_category_view import AbstractCategoryView
from bookkeeper.presenters.budget_presenter import BudgetPresenter
from bookkeeper.presenters.expense_presenter import ExpensePresenter
from bookkeeper.presenters.category_presenter import CategoryPresenter


class TestBudgetView(AbstractBudgetView):
    def add(self, bgt): pass
    def update(self, bgt): pass
    def handle_exceeding(self, bgts): pass


class TestExpenseView(AbstractExpenseView):
        def add(self, exp, cat_name): pass
        def update(self, exp, cat_name): pass
        def delete(self, pk): pass
        def add_category(self, cat): pass
        def update_category(self, cat): pass
        def delete_category(self, pk): pass


class TestCategoryView(AbstractCategoryView):
        def add(self, cat): pass
        def update(self, cat): pass
        def delete(self, pk): pass
        def warning(self, msg): pass


@pytest.fixture
def bgt_presenter():
    return BudgetPresenter(TestBudgetView(), MemoryRepository[Budget](), MemoryRepository[Expense]())


@pytest.fixture
def exp_presenter():
    return ExpensePresenter(TestExpenseView(), MemoryRepository[Expense](), MemoryRepository[Category](), bgt_presenter)


@pytest.fixture
def cat_presenter():
    return CategoryPresenter(TestCategoryView(), MemoryRepository[Category](), MemoryRepository[Expense](), exp_presenter)


def test_init(cat_presenter):
    pass
