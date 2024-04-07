""" This module contains presenter class for categories """

from bookkeeper.repository.abstract_repository import AbstractRepository

from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category

from bookkeeper.view.abstract_category_view import AbstractCategoryView

from bookkeeper.presenters.expense_presenter import ExpensePresenter


class CategoryPresenter:
    """
    Presenter class for categories. Implements logic of CRUD operations.
    """

    def __init__(self,
                 cat_view: AbstractCategoryView,
                 cat_repo: AbstractRepository[Category],
                 exp_repo: AbstractRepository[Expense],
                 exp_presenter: ExpensePresenter) -> None:
        self.cat_repo = cat_repo
        self.cat_view = cat_view
        self.exp_repo = exp_repo
        self.exp_presenter = exp_presenter
        for cat in self.cat_repo.get_all():
            self.cat_view.add(cat)
            self.exp_presenter.add_category(cat)

    def add(self, cat: Category) -> None:
        """
        Adds new category to repository and view and informs expense presenter.
        Called from category view.

        Parameters:
            cat - new Category object with empty pk
        """
        self.cat_repo.add(cat)
        self.cat_view.add(cat)
        self.exp_presenter.add_category(cat)

    def update(self, cat: Category) -> None:
        """
        Updates an existing category in repository and view and informs expense presenter.
        Called from category view.

        Parameters:
            cat - Category object from database
        """
        self.cat_repo.update(cat)
        self.cat_view.update(cat)
        self.exp_presenter.update_category(cat)
        exps_with_cat = self.exp_repo.get_all({'category': cat.pk})
        for exp in exps_with_cat:
            self.exp_presenter.update(exp)

    def delete(self, pk: int) -> None:
        """
        Deletes category by id from repository and view and informs expense presenter.
        If there are any expenses of this category informs user via category view.

        Parameters:
            pk - id of Category in database
        """
        exps_with_cat = self.exp_repo.get_all({'category': pk})
        if len(exps_with_cat) == 0:
            self.cat_repo.delete(pk)
            self.cat_view.delete(pk)
            self.exp_presenter.delete_category(pk)
        else:
            self.cat_view.warning(
                "Unable to remove category. There are expense(s) of this category.")
