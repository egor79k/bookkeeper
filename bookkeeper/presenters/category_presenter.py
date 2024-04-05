from bookkeeper.models.category import Category
from bookkeeper.repository.sqlite_repository import SQLiteRepository


class CategoryPresenter:
    def __init__(self, cat_view, cat_repo):
        self.cat_repo = cat_repo
        self.cat_view = cat_view
        for cat in self.cat_repo.get_all():
            self.cat_view.add(cat)


    def add(self, cat: Category) -> None:
        self.cat_repo.add(cat)
        self.cat_view.add(cat)


    def find_by_name(self, name: str) -> int | None:
        categories = self.cat_repo.get_all({'name': name})
        return categories[0].pk
