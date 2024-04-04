from abc import ABC, abstractmethod

from bookkeeper.models.expense import Expense
# from bookkeeper.presenters.expense_presenter import ExpensePresenter


class AbstractExpenseView(ABC):
    def set_presenter(self, exp_presenter) -> None:
        self.exp_presenter = exp_presenter


    @abstractmethod
    def add_expense(self, exp: Expense, cat_name: str) -> None:
        '''  '''


    @abstractmethod
    def update_expense(self, exp: Expense, cat_name: str) -> None:
        '''  '''


    @abstractmethod
    def delete_expense(self, pk: int) -> None:
        '''  '''
