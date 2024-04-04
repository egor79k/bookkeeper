from PySide6 import QtWidgets
from PySide6.QtCore import Slot

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

        # Connect slots to signals
        self.table.cellChanged.connect(self.on_table_cell_changed)
        self.add_button.clicked.connect(self.on_add_button_clicked)
        self.delete_button.clicked.connect(self.on_delete_button_clicked)

        # TEMP
        self.category_input.addItem("meat")
        self.add_expense(Expense(1237, 1, comment='Shopping', pk=1))


    def get_layout(self) -> QtWidgets.QLayout:
        return self.vbox_layout


    def add_expense(self, exp: Expense) -> None:
        if exp.pk == 0:
            raise ValueError('Trying to show object with empty `pk`')

        self.exp_row2pk.insert(0, exp.pk)
        self.table.insertRow(0)
        self.table.setItem(0, 0, QtWidgets.QTableWidgetItem(exp.expense_date.strftime('%Y-%m-%d %H:%M:%S')))
        self.table.setItem(0, 1, QtWidgets.QTableWidgetItem(str(exp.amount)))
        self.table.setItem(0, 2, QtWidgets.QTableWidgetItem(str(exp.category)))
        self.table.setItem(0, 3, QtWidgets.QTableWidgetItem(exp.comment))


    def update_all(self, exps: list[Expense]) -> None:
        for exp in exps:
            self.show_expense(exp)


    # @Slot()
    # def on_category_added(self, cat: Category) -> None:
    #     print("Emitted")


    @Slot()
    def on_table_cell_changed(self, row: int, column: int) -> None:
        print(row, column)


    @Slot()
    def on_add_button_clicked(self) -> None:
        print('Add button clicked')
        try:
            amount = float(self.amount_input.text())
            self.amount_input.clear()
        except:
            return

        cat_pk = self.cat_id2pk[self.category_input.currentIndex()]
        exp = Expense(amount, cat_pk)
        self.exp_presenter.add(exp)
        self.show_expense(expense)


    @Slot()
    def on_delete_button_clicked(self) -> None:
        print('Delete button clicked')
        exp_pk = self.row2pk[self.table.currentRow()]
        self.exp_presenter.delete(exp_pk) # NOT IMPLEMENTED
