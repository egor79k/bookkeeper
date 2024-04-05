from datetime import datetime, timedelta

from bookkeeper.repository.sqlite_repository import SQLiteRepository

from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense
# from bookkeeper.models.category import Category

from bookkeeper.view.abstract_budget_view import AbstractBudgetView

# from bookkeeper.presenters.expense_presenter import ExpensePresenter
# from bookkeeper.presenters.category_presenter import CategoryPresenter


class BudgetPresenter:
    def __init__(self, bgt_view: AbstractBudgetView, bgt_repo: SQLiteRepository[Budget], exp_repo: SQLiteRepository[Expense]):
        self.bgt_view = bgt_view
        self.bgt_repo = bgt_repo
        self.exp_repo = exp_repo


    def calculate_one(self, bgt: Budget, exps: list[Expense]) -> None:
        curr_dt = datetime.now()
        if 'day' == bgt.period:
            period = (datetime(curr_dt.year, curr_dt.month, curr_dt.day), curr_dt)
        elif 'week' == bgt.period:
            period = (datetime(curr_dt.year, curr_dt.month, curr_dt.day) - timedelta(days=dt.weekday()), curr_dt)
        elif 'month' == bgt.period:
            period = (datetime(curr_dt.year, curr_dt.month, 1), curr_dt)
        else:
            raise ValueError(f"Trying to calculate budget for unsupported period '{bgt.period}'")

        for exp in exps:
            if exp.expense_date >= period[0] and exp.expense_date <= period[1]:
                bgt.amount += exp.amount
        

    def calculate_all(self) -> None:
        exps = self.exp_repo.get_all()
        bgts = self.bgt_repo.get_all()

        for bgt in bgts:
            self.calculate_one(bgt)
