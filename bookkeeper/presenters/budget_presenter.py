from bookkeeper.models.budget import Budget
from bookkeeper.repository.sqlite_repository import SQLiteRepository


class BudgetPresenter:
    def __init__(self, bgt_view, bgt_repo):
        self.repo = bgt_repo
