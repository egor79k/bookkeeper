import pytest
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.view.abstract_budget_view import AbstractBudgetView
from bookkeeper.view.abstract_expense_view import AbstractExpenseView
from bookkeeper.presenters.budget_presenter import BudgetPresenter
from bookkeeper.presenters.expense_presenter import ExpensePresenter


class TestBudgetView(AbstractBudgetView):
    def add(self, bgt): pass
    def update(self, bgt): pass
    def handle_exceeding(self, bgts): pass


class TestExpenseView(AbstractExpenseView):
    added_exps = []
    updated_exps = []
    deleted_exps = []
    added_cats = []
    updated_cats = []
    deleted_cats = []

    def add(self, exp, cat_name):
        self.added_exps.append(exp)

    def update(self, exp, cat_name):
        self.updated_exps.append(exp)

    def delete(self, pk):
        self.deleted_exps.append(pk)

    def add_category(self, cat):
        self.added_cats.append(cat)

    def update_category(self, cat):
        self.updated_cats.append(cat)

    def delete_category(self, pk):
        self.deleted_cats.append(pk)


@pytest.fixture
def exp_view():
    return TestExpenseView()


@pytest.fixture
def exp_repo():
    return MemoryRepository[Expense]()


@pytest.fixture
def cat_repo():
    return MemoryRepository[Category]()


@pytest.fixture
def bgt_presenter():
    return BudgetPresenter(TestBudgetView(),
                           MemoryRepository[Budget](),
                           MemoryRepository[Expense]())


def test_init(exp_view, exp_repo, cat_repo, bgt_presenter):
    # Add some categories to repo
    cats = [
        Category('cat_1'),
        Category('cat_2')
    ]
    for cat in cats:
        cat_repo.add(cat)

    # Add some expenses to repo
    exps = [
        Expense(100, 1),
        Expense(200, 2)
    ]

    for exp in exps:
        exp_repo.add(exp)

    p = ExpensePresenter(exp_view, exp_repo, cat_repo, bgt_presenter)
    assert p.exp_view == exp_view
    assert p.exp_repo == exp_repo
    assert p.cat_repo == cat_repo
    assert p.bgt_presenter == bgt_presenter
    # Check all expenses were added to view
    assert exp_view.added_exps == exps

    # Check on unexisting category
    exp = Expense(300, 3)

    with pytest.raises(ValueError):
        p.add(exp)

    with pytest.raises(ValueError):
        p.update(exp)

    with pytest.raises(ValueError):
        ExpensePresenter(exp_view, exp_repo, cat_repo, bgt_presenter)


def test_crud(exp_view, exp_repo, cat_repo, bgt_presenter):
    p = ExpensePresenter(exp_view, exp_repo, cat_repo, bgt_presenter)
    cat_pk = cat_repo.add(Category('cat_1'))
    exp = Expense(100, cat_pk)

    # Check adding
    p.add(exp)
    assert exp in exp_repo.get_all()
    assert exp in exp_view.added_exps

    # Check updating unexisting
    with pytest.raises(ValueError):
        p.update(Expense(300, cat_pk, pk=100))

    # Check updating with restore
    new_exp = Expense(200, cat_pk, pk=exp.pk)
    p.update(new_exp, restore=True)
    assert exp_repo.get(exp.pk) == exp
    assert exp in exp_view.updated_exps

    # Check updating without restore
    new_exp = Expense(200, cat_pk, pk=exp.pk)
    p.update(new_exp, restore=False)
    assert exp_repo.get(exp.pk) == new_exp
    assert new_exp in exp_view.updated_exps

    # Check deleting unexisting
    with pytest.raises(KeyError):
        p.delete(100)

    # Check deleting
    p.delete(exp.pk)
    assert exp_repo.get(exp.pk) is None
    assert exp.pk in exp_view.deleted_exps


def test_crud_category(exp_view, exp_repo, cat_repo, bgt_presenter):
    p = ExpensePresenter(exp_view, exp_repo, cat_repo, bgt_presenter)
    cat = Category('cat_1')

    p.add_category(cat)
    assert cat in exp_view.added_cats

    p.update_category(cat)
    assert cat in exp_view.updated_cats

    p.delete_category(cat.pk)
    assert cat.pk in exp_view.deleted_cats
