from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.expense import Expense
from bookkeeper.view.abstract_expense_view import AbstractExpenseView
# from bookkeeper.presenters.expense_presenter import ExpensePresenter


class ExpensePresenter:
    def __init__(self, exp_view: AbstractExpenseView, exp_repo: SQLiteRepository[Expense]):
        self.repo = exp_repo


    def add(self, expense: Expense) -> None:
        print('Adding expense with amount:', expense.amount)
        self.repo.add(expense)
