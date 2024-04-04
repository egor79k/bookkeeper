from abc import ABC, abstractmethod

from bookkeeper.models.budget import Budget
from bookkeeper.presenters.budget_presenter import BudgetPresenter


class AbstractBudgetView(ABC):
    def set_presenter(self, bgt_presenter: BudgetPresenter) -> None:
        self.bgt_presenter = bgt_presenter


    @abstractmethod
    def add_budget(self, bgt: Budget) -> None:
        '''  '''


    @abstractmethod
    def update_all(self, bgts: list[Budget]) -> None:
        '''  '''
