from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QMainWindow

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.view.budget_view import BudgetView
from bookkeeper.view.expense_view import ExpenseView
from bookkeeper.view.category_view import CategoryView


class MainWindow(QMainWindow):
    def __init__(self, cat_view, exp_view, bgt_view):
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
        # self.cat_view.category_added.connect(self.exp_view.on_category_added)

        self.bgt_view = bgt_view
        vertical_layout.addLayout(self.bgt_view.get_layout(), 4)
        
        # vertical_layout.addWidget(QtWidgets.QLabel('Last expenses'))

        # expenses_table = QtWidgets.QTableWidget(20, 4)
        # vertical_layout.addWidget(expenses_table, 11)
        # expenses_table.setHorizontalHeaderLabels("Date Summ Category Comment".split())
        # header = expenses_table.horizontalHeader()
        # header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        # # expenses_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # expenses_table.verticalHeader().hide()

        # vertical_layout.addWidget(QtWidgets.QLabel('Budget'))

        # budget_table = QtWidgets.QTableWidget(3, 2)
        # vertical_layout.addWidget(budget_table, 4)
        # # budget_table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # budget_table.setHorizontalHeaderLabels("Summ Budget".split())
        # budget_table.setVerticalHeaderLabels("Day Week Month".split())
        # header = budget_table.horizontalHeader()
        # header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        # form_layout = QtWidgets.QFormLayout()
        # vertical_layout.addLayout(form_layout, 1)
        # form_layout.addRow(QtWidgets.QLabel('Summ'), QtWidgets.QLineEdit())
        # form_layout.addRow(QtWidgets.QLabel('Category'), QtWidgets.QComboBox())
        # add_expense_button = QtWidgets.QPushButton('Add')
        # form_layout.addRow(add_expense_button)
        # add_expense_button.clicked.connect(self.on_add_expense_button_click)

        # vertical_layout = QtWidgets.QVBoxLayout()
        # horizontal_layout.addLayout(vertical_layout, 1)
        
        # vertical_layout.addWidget(QtWidgets.QLabel('Categories'))

        # categories_tree = QtWidgets.QTreeWidget()
        # vertical_layout.addWidget(categories_tree)
        # categories_tree.setColumnCount(1)
        # categories_tree.setHeaderLabels(["Name"])

        # items = QtWidgets.QTreeWidgetItem('parent')
        # items.addChild(QtWidgets.QTreeWidgetItem('child'))
        # categories_tree.insertTopLevelItems(0, [items])
