import sys
from PySide6.QtWidgets import QApplication

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
    app = QApplication(sys.argv)

    # Connect MVP structure together
    bgt_repo = SQLiteRepository[Budget](Budget)
    exp_repo = SQLiteRepository[Expense](Expense)
    cat_repo = SQLiteRepository[Category](Category)
    bgt_view = BudgetView()
    exp_view = ExpenseView()
    cat_view = CategoryView()
    bgt_presenter = BudgetPresenter(bgt_view, bgt_repo)
    exp_presenter = ExpensePresenter(exp_view, exp_repo, cat_repo)
    cat_presenter = CategoryPresenter(cat_view, cat_repo, exp_presenter)
    bgt_view.set_presenter(bgt_presenter)
    exp_view.set_presenter(exp_presenter)
    cat_view.set_presenter(cat_presenter)

    window = MainWindow(cat_view, exp_view, bgt_view)
    window.show()
    sys.exit(app.exec())
