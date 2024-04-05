from abc import ABC, abstractmethod

from bookkeeper.models.category import Category
from bookkeeper.presenters.category_presenter import CategoryPresenter


class AbstractCategoryView(ABC):
    def set_presenter(self, cat_presenter: CategoryPresenter) -> None:
        self.cat_presenter = cat_presenter


    @abstractmethod
    def add(self, cat: Category) -> None:
        '''  '''


    @abstractmethod
    def update(self, cat: Category) -> None:
        '''  '''


    @abstractmethod
    def update_all(self, cats: list[Category]) -> None:
        '''  '''
