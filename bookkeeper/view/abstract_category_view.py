""" Contains declaration of the abstract base class for categories list view """

from abc import ABC, abstractmethod

from bookkeeper.models.category import Category


class AbstractCategoryView(ABC):
    """
    Abstract base class for categories list view.

    Attributes:
        cat_presenter - CategoryPresenter object implementing logic
    """

    cat_presenter = None

    def set_presenter(self, cat_presenter) -> None:
        """
        Sets presenter object for this view.

        Parameters:
            cat_presenter - CategoryPresenter object
        """
        self.cat_presenter = cat_presenter

    @abstractmethod
    def add(self, cat: Category) -> None:
        """
        Adds new category to view.

        Parameters:
            cat - Category object from database
        """

    @abstractmethod
    def update(self, cat: Category) -> None:
        """
        Updates an existing category data in the view.

        Parameters:
            cat - Category object from database
        """

    @abstractmethod
    def delete(self, pk: int) -> None:
        """
        Deletes category from view.

        Parameters:
            pk - id of Category object in database (primary key)
        """

    @abstractmethod
    def warning(self, msg: str) -> None:
        """
        Informs user about something.

        Parameters:
            msg - message string
        """
