from bookkeeper.models.category import Category
from bookkeeper.repository.sqlite_repository import SQLiteRepository


class CategoryPresenter:
    def __init__(self):
        self.repo = SQLiteRepository[Category](Category)


    def find_by_name(self, name: str) -> int | None:
        categories = self.repo.get_all({'name': name})
        return categories[0].pk
