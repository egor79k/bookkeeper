from datetime import datetime, timedelta

from bookkeeper.repository.abstract_repository import AbstractRepository

from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense
# from bookkeeper.models.category import Category

from bookkeeper.view.abstract_budget_view import AbstractBudgetView

# from bookkeeper.presenters.expense_presenter import ExpensePresenter
# from bookkeeper.presenters.category_presenter import CategoryPresenter


class BudgetPresenter:
    def __init__(self, bgt_view: AbstractBudgetView, bgt_repo: AbstractRepository[Budget], exp_repo: AbstractRepository[Expense]):
        self.bgt_view = bgt_view
        self.bgt_repo = bgt_repo
        self.exp_repo = exp_repo

        for bgt in self.bgt_repo.get_all():
            self.bgt_view.add(bgt)

        self.calculate_all()


    def calculate_one(self, bgt: Budget, exps: list[Expense]) -> None:
        curr_dt = datetime.now()
        if 'day' == bgt.period:
            period = (datetime(curr_dt.year, curr_dt.month, curr_dt.day), curr_dt)
        elif 'week' == bgt.period:
            period = (datetime(curr_dt.year, curr_dt.month, curr_dt.day) - timedelta(days=datetime.weekday(datetime.now())), curr_dt)
        elif 'month' == bgt.period:
            period = (datetime(curr_dt.year, curr_dt.month, 1), curr_dt)
        else:
            raise ValueError(f"Trying to calculate budget for unsupported period '{bgt.period}'")

        bgt.amount = 0
        for exp in exps:
            if exp.expense_date >= period[0] and exp.expense_date <= period[1]:
                bgt.amount += exp.amount
        

    def calculate_all(self) -> None:
        exps = self.exp_repo.get_all()
        bgts = self.bgt_repo.get_all()

        for bgt in bgts:
            self.calculate_one(bgt, exps)
            self.bgt_repo.update(bgt)
            self.bgt_view.update(bgt)


    def update(self, bgt: Budget, restore: bool = False):
        bgt_orig = self.bgt_repo.get(bgt.pk)

        if restore:
            bgt = bgt_orig
        else:
            bgt.amount = bgt_orig.amount
            bgt.period = bgt_orig.period
            self.bgt_repo.update(bgt)
            
        self.bgt_view.update(bgt)