from abc import ABC, abstractmethod

from bookkeeper.models.budget import Budget


class AbstractBudgetView(ABC):
    def set_presenter(self, bgt_presenter) -> None:
        self.bgt_presenter = bgt_presenter


    @abstractmethod
    def add(self, bgt: Budget) -> None:
        '''  '''


    @abstractmethod
    def update(self, bgt: Budget) -> None:
        '''  '''