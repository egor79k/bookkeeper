from PySide6 import QtWidgets
from PySide6.QtCore import Slot
from bookkeeper.presenters.expense_presenter import ExpensePresenter
from bookkeeper.presenters.category_presenter import CategoryPresenter
from bookkeeper.models.expense import Expense


class ExpenseView(QtWidgets.QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.expense_presenter = ExpensePresenter()
        self.category_presenter = CategoryPresenter()
        
        super().addWidget(QtWidgets.QLabel('Last expenses'))

        self.table = QtWidgets.QTableWidget(0, 4)
        super().addWidget(self.table)
        self.table.setHorizontalHeaderLabels("Date Summ Category Comment".split())
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        # self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().hide()

        form_layout = QtWidgets.QFormLayout()
        super().addLayout(form_layout)
        self.amount_input = QtWidgets.QLineEdit()
        self.category_input = QtWidgets.QComboBox()
        self.delete_button = QtWidgets.QPushButton('Delete')
        self.add_button = QtWidgets.QPushButton('Add')
        form_layout.addRow(QtWidgets.QLabel('Amount'), self.amount_input)
        form_layout.addRow(QtWidgets.QLabel('Category'), self.category_input)
        form_layout.addRow(self.delete_button, self.add_button)

        self.table.cellChanged.connect(self.on_table_cell_changed)
        self.add_button.clicked.connect(self.on_add_button_clicked)
        self.delete_button.clicked.connect(self.on_delete_button_clicked)

        # TEMP
        self.category_input.addItem("meat")
        self.add_expense(Expense(1237, 1, comment='Shopping'))


    def add_expense(self, expense: Expense) -> None:
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(expense.expense_date.strftime('%Y-%m-%d %H:%M:%S')))
        self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(expense.amount)))
        self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(expense.category)))
        self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(expense.comment))


    def update_table(self) -> None:
        expenses = self.expense_presenter.get_all() # NOT IMPLEMENTED
        for exp in expenses:
            self.add_expense(exp)


    @Slot()
    def on_table_cell_changed(self, row: int, column: int) -> None:
        print(row, column)


    @Slot()
    def on_add_button_clicked(self) -> None:
        print('Add button clicked')
        try:
            amount = float(self.amount_input.text())
        except:
            return

        print(amount)
        category_pk = self.category_presenter.find_by_name(self.category_input.currentText())
        expense = Expense(amount, category_pk)
        self.expense_presenter.add(expense)
        self.add_expense(expense)


    @Slot()
    def on_delete_button_clicked(self) -> None:
        print('Delete button clicked')
        self.expense_presenter.delete_by_order(self.table.currentRow()) # NOT IMPLEMENTED
        exp = Expense()
