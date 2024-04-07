""" Contains declaration of the abstract base class for budgets view """

from abc import ABC, abstractmethod

from bookkeeper.models.budget import Budget


class AbstractBudgetView(ABC):
    """
    Abstract base class for budgets view

    Attributes:
        bgt_presenter - BudgetPresenter object implementing logic
    """

    bgt_presenter = None

    def set_presenter(self, bgt_presenter) -> None:
        """
        Sets presenter object for this view

        Parameters:
            bgt_presenter - BudgetPresenter object
        """
        self.bgt_presenter = bgt_presenter

    @abstractmethod
    def add(self, bgt: Budget) -> None:
        """
        Adds new budget to view

        Parameters:
            bgt - Budget object from database
        """

    @abstractmethod
    def update(self, bgt: Budget) -> None:
        """
        Updates an existing budget data in the view.

        Parameters:
            bgt - Budget object from database
        """

    @abstractmethod
    def handle_exceeding(self, bgts: list[Budget]) -> None:
        """
        Implements reaction of view on exceeding budgets' limits.

        Parameters:
            bgts - list of Budget objects with exceeded limits
        """
