""" Contains class uniting all views in one window """

from PySide6 import QtWidgets

from bookkeeper.view.budget_view import BudgetView
from bookkeeper.view.expense_view import ExpenseView
from bookkeeper.view.category_view import CategoryView


class MainWindow(QtWidgets.QMainWindow):  # pylint: disable=too-few-public-methods
    """ Class uniting category, expense and budget views in one window """
    def __init__(self,
                 cat_view: CategoryView,
                 exp_view: ExpenseView,
                 bgt_view: BudgetView) -> None:
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
        vertical_layout.addLayout(self.exp_view.get_layout(), 10)

        self.bgt_view = bgt_view
        vertical_layout.addLayout(self.bgt_view.get_layout(), 3)
