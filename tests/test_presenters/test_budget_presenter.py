import pytest
from datetime import datetime, timedelta
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense
from bookkeeper.view.abstract_budget_view import AbstractBudgetView
from bookkeeper.presenters.budget_presenter import BudgetPresenter


class TestBudgetView(AbstractBudgetView):
    added_bgts = []
    updated_bgts = []
    handled_bgts = []

    def add(self, bgt):
        self.added_bgts.append(bgt)

    def update(self, bgt):
        self.updated_bgts.append(bgt)

    def handle_exceeding(self, bgts):
        self.handled_bgts += bgts


@pytest.fixture
def bgt_view():
    return TestBudgetView()


@pytest.fixture
def bgt_repo():
    return MemoryRepository[Budget]()


@pytest.fixture
def exp_repo():
    return MemoryRepository[Expense]()


@pytest.fixture
def bgt_presenter():
    return BudgetPresenter(TestBudgetView(), MemoryRepository[Budget](), MemoryRepository[Expense]())


def test_init(bgt_view, bgt_repo, exp_repo):
    bgts = [
        Budget(100, 1000, 'day'),
        Budget(1000, 10000, 'week'),
        Budget(10000, 100000, 'month'),
    ]

    for bgt in bgts:
        bgt_repo.add(bgt)

    p = BudgetPresenter(bgt_view, bgt_repo, exp_repo)

    assert p.bgt_view == bgt_view
    assert p.bgt_repo == bgt_repo
    assert p.exp_repo == exp_repo
    # Check that all budgets from repo were added to view
    assert bgt_view.added_bgts == bgts


def test_calculate_all_1(bgt_view, bgt_repo, exp_repo):
    # Add some expenses
    exp_repo.add(Expense(1, 0, datetime.now()))
    exp_repo.add(Expense(10, 0, datetime.now()))
    exp_repo.add(Expense(100, 0, datetime.now()))
    
    # Add budgets
    bgts = [
        Budget(0, 100, 'day'),
        Budget(0, 100, 'week'),
        Budget(0, 100, 'month')]

    for bgt in bgts:
        bgt_repo.add(bgt)

    p = BudgetPresenter(bgt_view, bgt_repo, exp_repo)
    p.calculate_all()
    
    # Check total sums
    assert 111 == bgt_repo.get(bgts[0].pk).amount
    assert 111 == bgt_repo.get(bgts[1].pk).amount
    assert 111 == bgt_repo.get(bgts[2].pk).amount


def test_calculate_all_2(bgt_view, bgt_repo, exp_repo):
    # Add some expenses
    exp_repo.add(Expense(1, 0, datetime.now()))
    exp_repo.add(Expense(10, 0, datetime.now()))
    exp_repo.add(Expense(100, 0, datetime.now() - timedelta(days=1)))
    exp_repo.add(Expense(1000, 0, datetime.now() - timedelta(days=10)))
    
    # Add budgets
    bgts = [
        Budget(0, 100, 'day'),
        Budget(0, 100, 'day')]

    for bgt in bgts:
        bgt_repo.add(bgt)

    p = BudgetPresenter(bgt_view, bgt_repo, exp_repo)
    p.calculate_all()
    
    # Check total sums
    assert 11 == bgt_repo.get(bgts[0].pk).amount
    assert 11 == bgt_repo.get(bgts[1].pk).amount


def test_calculate_all_3(bgt_view, bgt_repo, exp_repo):
    # Add some expenses
    exp_repo.add(Expense(1, 0, datetime.now()))
    exp_repo.add(Expense(10, 0, datetime.now()))
    exp_repo.add(Expense(100, 0, datetime.now() - timedelta(days=8)))
    exp_repo.add(Expense(1000, 0, datetime.now() - timedelta(days=100)))
    
    # Add budgets
    bgts = [
        Budget(0, 100, 'week'),
        Budget(0, 100, 'week')]

    for bgt in bgts:
        bgt_repo.add(bgt)

    p = BudgetPresenter(bgt_view, bgt_repo, exp_repo)
    p.calculate_all()
    
    # Check total sums
    assert 11 == bgt_repo.get(bgts[0].pk).amount
    assert 11 == bgt_repo.get(bgts[1].pk).amount


def test_calculate_all_4(bgt_view, bgt_repo, exp_repo):
    # Add some expenses
    exp_repo.add(Expense(1, 0, datetime.now()))
    exp_repo.add(Expense(10, 0, datetime.now()))
    exp_repo.add(Expense(100, 0, datetime.now() - timedelta(days=32)))
    exp_repo.add(Expense(1000, 0, datetime.now() - timedelta(days=1000)))
    
    # Add budgets
    bgts = [
        Budget(0, 100, 'month'),
        Budget(0, 100, 'month')]

    for bgt in bgts:
        bgt_repo.add(bgt)

    p = BudgetPresenter(bgt_view, bgt_repo, exp_repo)
    p.calculate_all()
    
    # Check total sums
    assert 11 == bgt_repo.get(bgts[0].pk).amount
    assert 11 == bgt_repo.get(bgts[1].pk).amount


def test_calculate_one(bgt_presenter):
    bgt = Budget(0, 1000, 'day')
    bgt_presenter.calculate_one(bgt, [
        Expense(1, 0, datetime.now() - timedelta(seconds=1)),
        Expense(10, 0, datetime.now() - timedelta(seconds=10)),
        Expense(100, 0, datetime.now() - timedelta(days=1)),
        Expense(1000, 0, datetime.now() - timedelta(days=2))])
    assert 11 == bgt.amount

    bgt = Budget(0, 1000, 'week')
    bgt_presenter.calculate_one(bgt, [
        Expense(1, 0, datetime.now() - timedelta(seconds=1)),
        Expense(10, 0, datetime.now() - timedelta(seconds=10)),
        Expense(100, 0, datetime.now() - timedelta(days=8)),
        Expense(1000, 0, datetime.now() - timedelta(days=10))])
    assert 11 == bgt.amount

    bgt = Budget(0, 1000, 'month')
    bgt_presenter.calculate_one(bgt, [
        Expense(1, 0, datetime.now() - timedelta(seconds=1)),
        Expense(10, 0, datetime.now() - timedelta(seconds=10)),
        Expense(100, 0, datetime.now() - timedelta(days=32)),
        Expense(1000, 0, datetime.now() - timedelta(days=40))])
    assert 11 == bgt.amount

    # Check for unsupported period
    with pytest.raises(ValueError):
        bgt_presenter.calculate_one(Budget(0, 0, 'year'), [])


def test_update(bgt_view, bgt_repo, exp_repo):
    # Add budgets
    bgts = [
        Budget(0, 100, 'day'),
        Budget(0, 100, 'week'),
        Budget(0, 100, 'month')]

    for bgt in bgts:
        bgt_repo.add(bgt)

    p = BudgetPresenter(bgt_view, bgt_repo, exp_repo)

    # Check with zero pk
    with pytest.raises(ValueError):
        p.update(Budget(0, 0))

    # Check with unknown pk
    with pytest.raises(ValueError):
        p.update(Budget(0, 0, pk=100))

    # Check that view and repo updates caused
    bgt = Budget(200, 1000, 'week', pk=bgts[0].pk)
    p.update(bgt, restore=True)
    assert bgts[0] == bgt_repo.get(bgt.pk)
    assert bgts[0] in bgt_view.updated_bgts
    assert bgts[0] not in bgt_view.handled_bgts

    # Check that view and repo updates caused
    bgt = Budget(2000, 1000, 'week', pk=bgts[0].pk)
    p.update(bgt, restore=False)
    assert bgt == bgt_repo.get(bgt.pk)
    assert bgt in bgt_view.updated_bgts
    assert bgt in bgt_view.handled_bgts
