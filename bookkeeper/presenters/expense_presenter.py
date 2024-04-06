from bookkeeper.repository.abstract_repository import AbstractRepository

from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category

from bookkeeper.view.abstract_expense_view import AbstractExpenseView

from bookkeeper.presenters.budget_presenter import BudgetPresenter


class ExpensePresenter:
    def __init__(self, exp_view: AbstractExpenseView, exp_repo: AbstractRepository[Expense], cat_repo: AbstractRepository[Category], bgt_presenter: BudgetPresenter) -> None:
        self.exp_view = exp_view
        self.exp_repo = exp_repo
        self.cat_repo = cat_repo
        self.bgt_presenter = bgt_presenter

        for exp in self.exp_repo.get_all():
            cat = self.cat_repo.get(exp.category)
            if cat is None:
                raise ValueError(f'Unknown category with pk {exp.category}')
            self.exp_view.add(exp, cat.name)


    def add(self, exp: Expense) -> None:
        self.exp_repo.add(exp)
        cat = self.cat_repo.get(exp.category)
        if cat is None:
            raise ValueError(f'Unknown category with pk {exp.category}')
        self.exp_view.add(exp, cat.name)
        self.bgt_presenter.calculate_all()


    def update(self, exp: Expense, restore: bool = False) -> None:
        exp_orig = self.exp_repo.get(exp.pk)
        
        if exp_orig is None:
            raise ValueError('Trying to update unexisting expense')

        cat = self.cat_repo.get(exp_orig.category)
        if cat is None:
            raise ValueError(f'Unknown category with pk {exp_orig.category}')
        exp.category = cat.pk

        if restore:
            exp = exp_orig
        else:
            self.exp_repo.update(exp)
            if exp.expense_date != exp_orig.expense_date or exp.amount != exp_orig.amount:
                self.bgt_presenter.calculate_all()
            
        self.exp_view.update(exp, cat.name)


    def delete(self, pk: int) -> None:
        self.exp_repo.delete(pk)
        self.exp_view.delete(pk)
        self.bgt_presenter.calculate_all()


    def add_category(self, cat: Category) -> None:
        self.exp_view.add_category(cat)


    def update_category(self, cat: Category) -> None:
        self.exp_view.update_category(cat)


    def delete_category(self, pk: int) -> None:
        self.exp_view.delete_category(pk)