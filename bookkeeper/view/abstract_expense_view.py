from abc import ABC, abstractmethod

from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category


class AbstractExpenseView(ABC):
    def set_presenter(self, exp_presenter) -> None:
        self.exp_presenter = exp_presenter


    @abstractmethod
    def add(self, exp: Expense, cat_name: str) -> None:
        '''  '''


    @abstractmethod
    def update(self, exp: Expense, cat_name: str) -> None:
        '''  '''


    @abstractmethod
    def delete(self, pk: int) -> None:
        '''  '''


    @abstractmethod
    def add_category(self, cat: Category) -> None:
        '''  '''


    @abstractmethod
    def update_category(self, cat: Category) -> None:
        '''  '''


    @abstractmethod
    def delete_category(self, pk: int) -> None:
        '''  '''
