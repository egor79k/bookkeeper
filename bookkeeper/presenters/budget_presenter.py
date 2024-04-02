from bookkeeper.models.budget import Budget
from bookkeeper.repository.sqlite_repository import SQLiteRepository


class BudgetPresenter:
    def __init__(self):
        self.repo = SQLiteRepository[Budget](Budget)
