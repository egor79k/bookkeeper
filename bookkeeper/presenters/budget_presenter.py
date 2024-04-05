from bookkeeper.repository.sqlite_repository import SQLiteRepository

from bookkeeper.models.budget import Budget
# from bookkeeper.models.expense import Expense
# from bookkeeper.models.category import Category

from bookkeeper.view.abstract_budget_view import AbstractBudgetView

# from bookkeeper.presenters.expense_presenter import ExpensePresenter
# from bookkeeper.presenters.category_presenter import CategoryPresenter


class BudgetPresenter:
    def __init__(self, bgt_view: AbstractBudgetView, bgt_repo: SQLiteRepository[Budget]):
        self.bgt_view = bgt_view
        self.bgt_repo = bgt_repo
        # self.bgt_view
