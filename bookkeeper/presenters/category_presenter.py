from bookkeeper.models.category import Category
from bookkeeper.repository.sqlite_repository import SQLiteRepository


class CategoryPresenter:
    def __init__(self, cat_view, cat_repo, exp_repo, exp_presenter):
        self.cat_repo = cat_repo
        self.cat_view = cat_view
        self.exp_repo = exp_repo
        self.exp_presenter = exp_presenter
        for cat in self.cat_repo.get_all():
            self.cat_view.add(cat)
            self.exp_presenter.add_category(cat)


    def add(self, cat: Category) -> None:
        self.cat_repo.add(cat)
        self.cat_view.add(cat)
        self.exp_presenter.add_category(cat)


    def update(self, cat: Category) -> None:
        self.cat_repo.update(cat)
        self.cat_view.update(cat)
        self.exp_presenter.update_category(cat)


    def delete(self, pk: int) -> None:
        exps_with_cat = self.exp_repo.get_all({'category': pk})
        if len(exps_with_cat) == 0:
            self.cat_repo.delete(pk)
            self.cat_view.delete(pk)
            self.exp_presenter.delete_category(pk)
        else:
            print(f"Unable to remove category. There are an expense(s) of this category.")


    def find_by_name(self, name: str) -> int | None:
        categories = self.cat_repo.get_all({'name': name})
        return categories[0].pk
