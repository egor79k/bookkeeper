from bookkeeper.repository.sqlite_repository import SQLiteRepository

from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category

from bookkeeper.view.abstract_expense_view import AbstractExpenseView


class ExpensePresenter:
    def __init__(self, exp_view: AbstractExpenseView, exp_repo: SQLiteRepository[Expense], cat_repo: SQLiteRepository[Category]) -> None:
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
        exp_orig = self.exp_repo.get(exp.pk)
        cat = self.cat_repo.get(exp_orig.category)
        exp.category = cat.pk

        if restore:
            exp = exp_orig
        else:
            self.exp_repo.update(exp)
            
        self.exp_view.update_expense(exp, cat.name)


    def delete(self, pk: int) -> None:
        self.exp_repo.delete(pk)
        self.exp_view.delete_expense(pk)


    def add_category(self, cat: Category) -> None:
        self.exp_view.add_category(cat)


    def update_category(self, cat: Category) -> None:
        self.exp_view.update_category(cat)


    def delete_category(self, pk: int) -> None:
        self.exp_view.delete_category(pk)