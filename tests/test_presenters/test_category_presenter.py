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
        added_cats = []
        updated_cats = []
        deleted_cats = []
        warnings = []

        def add(self, cat):
            self.added_cats.append(cat)

        def update(self, cat):
            self.updated_cats.append(cat)

        def delete(self, pk):
            self.deleted_cats.append(pk)

        def warning(self, msg):
            self.warnings.append(msg)


@pytest.fixture
def cat_view():
    return TestCategoryView()


@pytest.fixture
def cat_repo():
    return MemoryRepository[Category]()


@pytest.fixture
def exp_view():
    return TestExpenseView()


@pytest.fixture
def exp_repo():
    return MemoryRepository[Expense]()


@pytest.fixture
def bgt_presenter():
    return BudgetPresenter(TestBudgetView(), MemoryRepository[Budget](), MemoryRepository[Expense]())


@pytest.fixture
def exp_presenter():
    return ExpensePresenter(TestExpenseView(), MemoryRepository[Expense](), MemoryRepository[Category](), bgt_presenter)


def test_init(cat_view, cat_repo, exp_repo, exp_presenter):
    # Add some categories to repo
    cats = [
        Category('cat_1'),
        Category('cat_2')
    ]
    for cat in cats:
        cat_repo.add(cat)

    p = CategoryPresenter(cat_view, cat_repo, exp_repo, exp_presenter)
    assert p.cat_view == cat_view
    assert p.cat_repo == cat_repo
    assert p.exp_repo == exp_repo
    assert p.exp_presenter == exp_presenter
    # Check that all categories were added to view
    assert cat_view.added_cats == cats


def test_crud(cat_view, exp_view, cat_repo, exp_repo, bgt_presenter):
    exp_presenter = ExpensePresenter(exp_view, exp_repo, cat_repo, bgt_presenter)
    p = CategoryPresenter(cat_view, cat_repo, exp_repo, exp_presenter)

    # Check adding    
    cat = Category('cat_1')
    p.add(cat)
    assert cat in cat_repo.get_all()
    assert cat in cat_view.added_cats

    # Add expenses of this category
    exp_repo.add(Expense(100, cat.pk))
    exp_repo.add(Expense(200, cat.pk))

    # Check updating
    p.update(cat)
    assert cat in cat_view.updated_cats

    # Check deleting unexisting
    with pytest.raises(KeyError):
        p.delete(100)

    # Check deleting
    cat1 = Category('cat_2')
    p.add(cat1)
    assert cat1 in cat_repo.get_all()
    p.delete(cat1.pk)
    assert cat1 not in cat_repo.get_all()
    assert cat1.pk in cat_view.deleted_cats
    assert len(cat_view.warnings) == 0

    # Check deleting category with expenses
    p.delete(cat.pk)
    assert cat.pk not in cat_view.deleted_cats
    assert len(cat_view.warnings) == 1
