''' Main script running the GUI version '''
import sys
from PySide6 import QtWidgets

from bookkeeper.repository.sqlite_repository import SQLiteRepository

from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category

from bookkeeper.view.main_window import MainWindow
from bookkeeper.view.budget_view import BudgetView
from bookkeeper.view.expense_view import ExpenseView
from bookkeeper.view.category_view import CategoryView

from bookkeeper.presenters.budget_presenter import BudgetPresenter
from bookkeeper.presenters.expense_presenter import ExpensePresenter
from bookkeeper.presenters.category_presenter import CategoryPresenter

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    DB_FILE = 'bookkeeper.db'

    # Connect MVP structure together
    bgt_repo = SQLiteRepository[Budget](Budget, DB_FILE)
    exp_repo = SQLiteRepository[Expense](Expense, DB_FILE)
    cat_repo = SQLiteRepository[Category](Category, DB_FILE)

    # Init budget table in case of empty database
    for period, amount in (('month', 30000), ('week', 7000), ('day', 1000)):
        if len(bgt_repo.get_all({'period': period})) == 0:
            bgt_repo.add(Budget(0, amount, period))

    bgt_view = BudgetView()
    exp_view = ExpenseView()
    cat_view = CategoryView()
    bgt_presenter = BudgetPresenter(bgt_view, bgt_repo, exp_repo)
    exp_presenter = ExpensePresenter(exp_view, exp_repo, cat_repo, bgt_presenter)
    cat_presenter = CategoryPresenter(cat_view, cat_repo, exp_repo, exp_presenter)
    bgt_view.set_presenter(bgt_presenter)
    exp_view.set_presenter(exp_presenter)
    cat_view.set_presenter(cat_presenter)

    window = MainWindow(cat_view, exp_view, bgt_view)
    window.show()
    sys.exit(app.exec())
