from abc import ABC, abstractmethod

from bookkeeper.models.category import Category


class AbstractCategoryView(ABC):
    def set_presenter(self, cat_presenter) -> None:
        self.cat_presenter = cat_presenter


    @abstractmethod
    def add(self, cat: Category) -> None:
        '''  '''


    @abstractmethod
    def update(self, cat: Category) -> None:
        '''  '''


    @abstractmethod
    def delete(self, pk: int) -> None:
        '''  '''


    @abstractmethod
    def warning(self, msg: str) -> None:
        '''  '''
