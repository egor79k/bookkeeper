from abc import ABC, abstractmethod

from bookkeeper.models.expense import Expense
# from bookkeeper.presenters.expense_presenter import ExpensePresenter


class AbstractExpenseView(ABC):
    def set_presenter(self, exp_presenter) -> None:
        self.exp_presenter = exp_presenter


    @abstractmethod
    def add_expense(self, exp: Expense) -> None:
        '''  '''


    @abstractmethod
    def update_all(self, exps: list[Expense]) -> None:
        '''  '''
