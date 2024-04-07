""" Contains implementation of the class for expenses list GUI """

from datetime import datetime
from PySide6 import QtWidgets, QtCore

from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category

from bookkeeper.view.abstract_expense_view import AbstractExpenseView


class ExpenseView(AbstractExpenseView):
    """
    This class implements a GUI for expenses table, allowing user
    to create, list, update and delete expenses from database.
    It also maintains an actual list of categories, allowing user to choose it
    when adding new expense operation.
    It is a part of MVP architecture so it handles link to expense presenter.
    Therefore set_presenter() method of abstract base class must be called
    before calling any other methods.
    All user actions are passed to presenter and don't cause any changes
    in UI directly. Presenter calls back to this view to display changes
    in UI after doing necessary logic.

    Attributes:
        exp_row2pk - list matching expense's row in table to it's pk in database
        cat_id2pk  - list matching category's id in combo box to it's pk in database
    """

    exp_row2pk: list[int]
    cat_id2pk: list[int]

    def __init__(self) -> None:
        self.exp_row2pk = []
        self.cat_id2pk = []

        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.vbox_layout.addWidget(QtWidgets.QLabel('Last expenses'))

        self.table = QtWidgets.QTableWidget(0, 4)
        self.vbox_layout.addWidget(self.table)
        self.table.setHorizontalHeaderLabels("Date Amount Category Comment".split())
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.table.verticalHeader().hide()

        form_layout = QtWidgets.QFormLayout()
        self.vbox_layout.addLayout(form_layout)
        self.amount_input = QtWidgets.QLineEdit()
        self.category_input = QtWidgets.QComboBox()
        delete_button = QtWidgets.QPushButton('Delete')
        add_button = QtWidgets.QPushButton('Add')
        form_layout.addRow(QtWidgets.QLabel('Amount'), self.amount_input)
        form_layout.addRow(QtWidgets.QLabel('Category'), self.category_input)
        form_layout.addRow(delete_button, add_button)

        # Connect signals to slots
        add_button.clicked.connect(self.on_add_button_clicked)
        delete_button.clicked.connect(self.on_delete_button_clicked)
        self.table.cellChanged.connect(self.on_table_cell_changed)

    def get_layout(self) -> QtWidgets.QLayout:
        """
        Get layout to insert expenses widgets into window

        Returns:
            QLayout object containing expense UI
        """
        return self.vbox_layout

    def add(self, exp: Expense, cat_name: str) -> None:
        """
        Adds new expense to view. Creates new row in the top of the table.

        Parameters:
            exp      - Expense object from database
            cat_name - Category name according to category pk in exp
        """
        if exp.pk == 0:
            raise ValueError('Trying to show object with empty `pk`')

        self.exp_row2pk.insert(0, exp.pk)
        self.table.blockSignals(True)
        self.table.insertRow(0)
        date_str = exp.expense_date.strftime('%Y-%m-%d %H:%M')
        self.table.setItem(0, 0, QtWidgets.QTableWidgetItem(date_str))
        self.table.setItem(0, 1, QtWidgets.QTableWidgetItem(str(exp.amount)))
        cat_item = QtWidgets.QTableWidgetItem(cat_name)
        cat_item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.table.setItem(0, 2, cat_item)
        self.table.setItem(0, 3, QtWidgets.QTableWidgetItem(exp.comment))
        self.table.blockSignals(False)

    def update(self, exp: Expense, cat_name: str) -> None:
        """
        Updates an existing expense data in the table.

        Parameters:
            exp - Expense object from database
            cat_name - Category name according to category pk in exp
        """
        row = self.exp_row2pk.index(exp.pk)
        self.table.item(row, 0).setText(exp.expense_date.strftime('%Y-%m-%d %H:%M'))
        self.table.item(row, 1).setText(str(exp.amount))
        self.table.item(row, 2).setText(cat_name)
        self.table.item(row, 3).setText(exp.comment)

    def delete(self, pk: int) -> None:
        """
        Deletes expense from table.

        Parameters:
            pk - id of Expense object in database (primary key)
        """
        row = self.exp_row2pk.index(pk)
        self.exp_row2pk.pop(row)
        self.table.removeRow(row)

    def add_category(self, cat: Category) -> None:
        """
        Adds new category to combo box.

        Parameters:
            cat - Category object from database
        """
        self.cat_id2pk.append(cat.pk)
        self.category_input.addItem(cat.name)

    def update_category(self, cat: Category) -> None:
        """
        Updates an existing category in the combo box.

        Parameters:
            cat - Category object from database
        """
        index = self.cat_id2pk.index(cat.pk)
        self.category_input.setItemText(index, cat.name)

    def delete_category(self, pk: int) -> None:
        """
        Deletes category from combo box by its pk.

        Parameters:
            pk - id of Category object in database (primary key)
        """
        index = self.cat_id2pk.index(pk)
        self.cat_id2pk.pop(index)
        self.category_input.removeItem(index)

    @QtCore.Slot()
    def on_table_cell_changed(self, row: int, _: int) -> None:
        """
        Handles editing expense data in the table.
        Passes updated Expense object to presenter.
        If user input had invalid format requests to restore previous expense's data.
        Does not change view. All changes in UI are caused by the presenter.

        Parameters:
            row - row of changed item in the table
            _   - column of changed item in the table (not used)
        """
        restore = False

        # Get date from table
        try:
            val = self.table.item(row, 0).text()
            date = datetime.fromisoformat(val)
        except ValueError:
            date = datetime.now()
            restore = True

        # Get amount from table
        try:
            val = self.table.item(row, 1).text()
            amount = int(val)
        except ValueError:
            amount = 0
            restore = True

        # Get comment from table
        comment = self.table.item(row, 3).text()
        pk = self.exp_row2pk[row]
        exp = Expense(amount, expense_date=date, comment=comment, pk=pk)
        self.exp_presenter.update(exp, restore)

    @QtCore.Slot()
    def on_add_button_clicked(self) -> None:
        """
        Handles click on add button passing new expense to presenter.
        If user input has invalid format does nothing.
        Does not change view. All changes in UI are caused by the presenter.
        """
        try:
            amount = int(self.amount_input.text())
            self.amount_input.clear()
        except ValueError:
            return

        cat_pk = self.cat_id2pk[self.category_input.currentIndex()]
        exp = Expense(amount, cat_pk)
        self.exp_presenter.add(exp)

    @QtCore.Slot()
    def on_delete_button_clicked(self) -> None:
        """
        Handles click on delete button passing pk of the expense being deleted
        to the presenter.
        Does not change view. All changes in UI are caused by the presenter.
        """
        rows = {index.row() for index in self.table.selectedIndexes()}
        exp_pks = [self.exp_row2pk[row] for row in rows]
        for exp_pk in exp_pks:
            self.exp_presenter.delete(exp_pk)
