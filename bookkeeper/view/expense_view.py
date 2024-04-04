from datetime import datetime
from PySide6 import QtWidgets
from PySide6.QtCore import Qt, Slot

from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category

from bookkeeper.view.abstract_expense_view import AbstractExpenseView

from bookkeeper.presenters.expense_presenter import ExpensePresenter
from bookkeeper.presenters.category_presenter import CategoryPresenter


class ExpenseView(AbstractExpenseView):
    def __init__(self):
        # self.exp_presenter = ExpensePresenter()
        self.category_presenter = CategoryPresenter(None, None)
        self.exp_row2pk = []
        self.cat_id2pk = []
        
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.vbox_layout.addWidget(QtWidgets.QLabel('Last expenses'))

        self.table = QtWidgets.QTableWidget(0, 4)
        self.vbox_layout.addWidget(self.table)
        self.table.setHorizontalHeaderLabels("Date Summ Category Comment".split())
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        # self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().hide()

        form_layout = QtWidgets.QFormLayout()
        self.vbox_layout.addLayout(form_layout)
        self.amount_input = QtWidgets.QLineEdit()
        self.category_input = QtWidgets.QComboBox()
        self.delete_button = QtWidgets.QPushButton('Delete')
        self.add_button = QtWidgets.QPushButton('Add')
        form_layout.addRow(QtWidgets.QLabel('Amount'), self.amount_input)
        form_layout.addRow(QtWidgets.QLabel('Category'), self.category_input)
        form_layout.addRow(self.delete_button, self.add_button)

        # TEMP
        self.category_input.addItem("meat")
        self.cat_id2pk = [1]


    def set_presenter(self, exp_presenter) -> None:
        self.exp_presenter = exp_presenter

        # Connect slots to signals after presenter filled table
        self.table.cellChanged.connect(self.on_table_cell_changed)
        self.add_button.clicked.connect(self.on_add_button_clicked)
        self.delete_button.clicked.connect(self.on_delete_button_clicked)


    def get_layout(self) -> QtWidgets.QLayout:
        return self.vbox_layout


    def add_expense(self, exp: Expense, cat_name: str) -> None:
        if exp.pk == 0:
            raise ValueError('Trying to show object with empty `pk`')

        self.exp_row2pk.insert(0, exp.pk)
        self.table.insertRow(0)
        self.table.setItem(0, 0, QtWidgets.QTableWidgetItem(exp.expense_date.strftime('%Y-%m-%d %H:%M:%S')))
        self.table.setItem(0, 1, QtWidgets.QTableWidgetItem(str(exp.amount)))
        cat_item = QtWidgets.QTableWidgetItem(cat_name)
        cat_item.setFlags(Qt.ItemIsEnabled)
        self.table.setItem(0, 2, cat_item)
        self.table.setItem(0, 3, QtWidgets.QTableWidgetItem(exp.comment))


    def update_expense(self, exp: Expense, cat_name: str) -> None:
        row = self.exp_row2pk.index(exp.pk)
        self.table.item(row, 0).setText(exp.expense_date.strftime('%Y-%m-%d %H:%M:%S'))
        self.table.item(row, 1).setText(str(exp.amount))
        self.table.item(row, 2).setText(cat_name)
        self.table.item(row, 3).setText(exp.comment)


    def delete_expense(self, pk: int) -> None:
        row = self.exp_row2pk.index(pk)
        self.exp_row2pk.pop(row)
        self.table.removeRow(row)


    def update_all(self, exps: list[Expense]) -> None:
        pass


    @Slot()
    def on_table_cell_changed(self, row: int, column: int) -> None:
        restore = False

        # Get date from table
        try:
            val = self.table.itemAt(row, 0).text()
            date = datetime.strptime(val, '%Y-%m-%d %H:%M:%S')
        except:
            print('Fail date')
            date = None
            restore = True

        # Get amount from table
        try:
            val = self.table.itemAt(row, 1).text()
            print(val)
            amount = int(val)
        except:
            print('Fail amount', val)
            amount = None
            restore = True

        # Get comment from table
        comment = self.table.itemAt(row, 3).text()
        pk = self.exp_row2pk[row]
        exp = Expense(amount, expense_date=date, comment=comment, pk=pk)
        self.exp_presenter.update(exp, restore)


    @Slot()
    def on_add_button_clicked(self) -> None:
        print('Add button clicked')
        try:
            amount = int(self.amount_input.text())
            self.amount_input.clear()
        except:
            return

        cat_pk = self.cat_id2pk[self.category_input.currentIndex()]
        exp = Expense(amount, cat_pk)
        self.exp_presenter.add(exp)


    @Slot()
    def on_delete_button_clicked(self) -> None:
        print('Delete button clicked')
        exp_pk = self.exp_row2pk[self.table.currentRow()]
        self.exp_presenter.delete(exp_pk)
