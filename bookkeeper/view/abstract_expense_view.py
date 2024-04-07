""" Contains declaration of the abstract base class for expenses list view """

from abc import ABC, abstractmethod

from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category


class AbstractExpenseView(ABC):
    """
    Abstract base class for categories list view

    Attributes:
        exp_presenter - ExpensePresenter object implementing logic
    """

    exp_presenter = None

    def set_presenter(self, exp_presenter) -> None:
        """
        Sets presenter object for this view

        Parameters:
            exp_presenter - ExpensePresenter object
        """
        self.exp_presenter = exp_presenter


    @abstractmethod
    def add(self, exp: Expense, cat_name: str) -> None:
        """
        Adds new expense to view.

        Parameters:
            exp - Expense object from database
        """


    @abstractmethod
    def update(self, exp: Expense, cat_name: str) -> None:
        """
        Updates an existing expense data in the view.

        Parameters:
            exp - Expense object from database
        """


    @abstractmethod
    def delete(self, pk: int) -> None:
        """
        Deletes expense from view.

        Parameters:
            pk - id of Expense object in database (primary key)
        """


    @abstractmethod
    def add_category(self, cat: Category) -> None:
        """
        Adds new category to view.

        Parameters:
            cat - Category object from database
        """


    @abstractmethod
    def update_category(self, cat: Category) -> None:
        """
        Updates an existing category data in the view.

        Parameters:
            cat - Category object from database
        """


    @abstractmethod
    def delete_category(self, pk: int) -> None:
        """
        Deletes category from view.

        Parameters:
            pk - id of Category object in database (primary key)
        """
