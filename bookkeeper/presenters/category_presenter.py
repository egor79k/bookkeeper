from bookkeeper.models.category import Category
from bookkeeper.repository.sqlite_repository import SQLiteRepository


class CategoryPresenter:
    def __init__(self, cat_view, cat_repo):
        self.repo = cat_repo


    def find_by_name(self, name: str) -> int | None:
        categories = self.repo.get_all({'name': name})
        return categories[0].pk
