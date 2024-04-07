""" This module contains presenter class for expenses """

from bookkeeper.repository.abstract_repository import AbstractRepository

from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category

from bookkeeper.view.abstract_expense_view import AbstractExpenseView

from bookkeeper.presenters.budget_presenter import BudgetPresenter


class ExpensePresenter:
    """
    Presenter class for expenses.
    Implements logic of CRUD operations and categories list updating.
    """

    def __init__(self,
                 exp_view: AbstractExpenseView,
                 exp_repo: AbstractRepository[Expense],
                 cat_repo: AbstractRepository[Category],
                 bgt_presenter: BudgetPresenter) -> None:
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
        """
        Adds new expense to repository and view
        and causes budget presenter to recalculate sums.
        Called from expense view.

        Parameters:
            exp - new Expense object with empty pk
        """
        self.exp_repo.add(exp)
        cat = self.cat_repo.get(exp.category)
        if cat is None:
            raise ValueError(f'Unknown category with pk {exp.category}')
        self.exp_view.add(exp, cat.name)
        self.bgt_presenter.calculate_all()


    def update(self, exp: Expense, restore: bool = False) -> None:
        """
        Updates an existing expense operation in repository and view
        and causes budget presenter to recalculate sums.
        Called from expense view.

        Parameters:
            exp - Expense object from database
        """
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
        """
        Deletes expense operation by id from repository and view
        and causes budget presenter to recalculate sums.

        Parameters:
            pk - id of Expense in database
        """
        self.exp_repo.delete(pk)
        self.exp_view.delete(pk)
        self.bgt_presenter.calculate_all()


    def add_category(self, cat: Category) -> None:
        """
        Adds new category to expense view.
        Called by category presenter.

        Parameters:
            cat - Category object from database
        """
        self.exp_view.add_category(cat)


    def update_category(self, cat: Category) -> None:
        """
        Updates category in expense view.
        Called by category presenter.

        Parameters:
            cat - Category object from database
        """
        self.exp_view.update_category(cat)


    def delete_category(self, pk: int) -> None:
        """
        Deletes category from expense view.
        Called by category presenter.

        Parameters:
            pk - id of Category object in database
        """
        self.exp_view.delete_category(pk)
