from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.view.abstract_expense_view import AbstractExpenseView


class ExpensePresenter:
    def __init__(self, exp_view: AbstractExpenseView, exp_repo: SQLiteRepository[Expense], cat_repo: SQLiteRepository[Category]):
        self.exp_view = exp_view
        self.exp_repo = exp_repo
        self.cat_repo = cat_repo
        for exp in self.exp_repo.get_all():
            cat = self.cat_repo.get(exp.category)
            self.exp_view.add_expense(exp, cat.name)


    def add(self, exp: Expense) -> None:
        self.exp_repo.add(exp)
        cat = self.cat_repo.get(exp.category)
        self.exp_view.add_expense(exp, cat.name)


    def update(self, exp: Expense, restore: bool = False):
        if restore:
            exp = self.exp_repo.get(exp.pk)
        else:
            self.exp_repo.update(exp)

        cat = self.cat_repo.get(exp.category)
        self.exp_view.update_expense(exp, cat.name)


    def delete(self, pk: int) -> None:
        self.exp_repo.delete(pk)
        self.exp_view.delete_expense(pk)