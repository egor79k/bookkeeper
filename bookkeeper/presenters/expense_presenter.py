from bookkeeper.models.expense import Expense
from bookkeeper.repository.sqlite_repository import SQLiteRepository


class ExpensePresenter:
    def __init__(self):
        self.repo = SQLiteRepository[Expense](Expense)


    def add(self, expense: Expense) -> None:
        print('Adding expense with amount:', expense.amount)
        self.repo.add(expense)
