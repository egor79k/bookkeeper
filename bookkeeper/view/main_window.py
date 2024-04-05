from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QMainWindow

from bookkeeper.repository.sqlite_repository import SQLiteRepository

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense

from bookkeeper.view.budget_view import BudgetView
from bookkeeper.view.expense_view import ExpenseView
from bookkeeper.view.category_view import CategoryView


class MainWindow(QMainWindow):
    def __init__(self, cat_view: CategoryView, exp_view: ExpenseView, bgt_view: BudgetView) -> None:
        super().__init__()
        self.setWindowTitle('Bookkeeper')
        self.resize(800, 600)
        
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        horizontal_layout = QtWidgets.QHBoxLayout()
        central_widget.setLayout(horizontal_layout)
        vertical_layout = QtWidgets.QVBoxLayout()
        horizontal_layout.addLayout(vertical_layout, 3)

        self.cat_view = cat_view
        horizontal_layout.addLayout(self.cat_view.get_layout())
        
        self.exp_view = exp_view
        vertical_layout.addLayout(self.exp_view.get_layout(), 11)

        self.bgt_view = bgt_view
        vertical_layout.addLayout(self.bgt_view.get_layout(), 4)
        