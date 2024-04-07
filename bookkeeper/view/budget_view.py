""" Contains class implementing the GUI for budgets """

from PySide6 import QtWidgets, QtCore, QtGui

from bookkeeper.models.budget import Budget

from bookkeeper.view.abstract_budget_view import AbstractBudgetView


class BudgetView(AbstractBudgetView):
    """
    This class implements a GUI for budgets table, allowing user
    to view current budgets and set its limits.
    It is a part of MVP architecture so it handles link to budget presenter.
    Therefore set_presenter() method of abstract base class must be called
    before calling any other methods.
    All user actions are passed to presenter and don't cause any changes
    in UI directly. Presenter calls back to this view to display changes
    in UI after doing necessary logic.

    Attributes:
        row2pk - list matching budget's row in table to it's pk in database
    """

    row2pk: list[int]

    def __init__(self) -> None:
        self.row2pk = []

        self.exceeding_brush = QtGui.QBrush(QtGui.QColor('DarkRed'))

        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.vbox_layout.addWidget(QtWidgets.QLabel('Budget'))

        self.table = QtWidgets.QTableWidget(0, 2)
        self.vbox_layout.addWidget(self.table, 4)
        # self.table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table.setHorizontalHeaderLabels(('Sum', 'Budget'))
        # self.table.setVerticalHeaderLabels("Day Week Month".split())
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        # Connect signals to slots
        self.table.cellChanged.connect(self.on_table_cell_changed)

    def get_layout(self) -> QtWidgets.QLayout:
        """
        Get layout to insert budgets widgets into window

        Returns:
            QLayout object containing expense UI
        """
        return self.vbox_layout

    def add(self, bgt: Budget) -> None:
        """
        Adds new budget to view. Creates new item in categories tree.

        Parameters:
            bgt - Budget object from database
        """
        if bgt.pk == 0:
            raise ValueError('Trying to show object with empty `pk`')

        self.row2pk.insert(0, bgt.pk)
        self.table.blockSignals(True)
        self.table.insertRow(0)
        self.table.setVerticalHeaderItem(0, QtWidgets.QTableWidgetItem(bgt.period))
        amount_item = QtWidgets.QTableWidgetItem(str(bgt.amount))
        amount_item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.table.setItem(0, 0, amount_item)
        self.table.setItem(0, 1, QtWidgets.QTableWidgetItem(str(bgt.limit)))
        self.table.blockSignals(False)

    def update(self, bgt: Budget) -> None:
        """
        Updates an existing budget data in the table.

        Parameters:
            bgt - Budget object from database
        """
        row = self.row2pk.index(bgt.pk)
        self.table.blockSignals(True)
        self.table.setVerticalHeaderItem(row, QtWidgets.QTableWidgetItem(bgt.period))
        item = self.table.item(row, 0)
        item.setText(str(bgt.amount))
        item.setData(QtCore.Qt.BackgroundRole, None)
        item = self.table.item(row, 1)
        item.setText(str(bgt.limit))
        item.setData(QtCore.Qt.BackgroundRole, None)
        self.table.blockSignals(False)

    def handle_exceeding(self, bgts: list[Budget]) -> None:
        """
        Implements reaction of view on exceeding budgets' limits.
        Paints red exceeded budget in table and causes a pop-up window with warning.

        Parameters:
            bgts - list of Budget objects with exceeded limits
        """
        self.table.blockSignals(True)
        for bgt in bgts:
            row = self.row2pk.index(bgt.pk)
            self.table.item(row, 0).setBackground(self.exceeding_brush)
            self.table.item(row, 1).setBackground(self.exceeding_brush)
        self.table.blockSignals(False)

        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle("Budget warning")
        periods = [bgt.period for bgt in bgts]
        msg_box.setText("Budget was exceeded for " + ", ".join(periods))
        msg_box.exec()

    @QtCore.Slot()
    def on_table_cell_changed(self, row: int, _: int) -> None:
        """
        Handles editing budget data (only limit) in the table.
        Passes updated Budget object to presenter.
        If user input had invalid format requests to restore previous budget's data.
        Does not change view. All changes in UI are caused by the presenter.

        Parameters:
            row - row of changed item in the table
            _   - column of changed item in the table (not used)
        """
        restore = False

        bgt = Budget()

        # Get period from table
        bgt.period = self.table.verticalHeaderItem(row).text()

        # Get sum from table
        bgt.amount = int(self.table.item(row, 0).text())

        # Get limit from table
        try:
            val = self.table.item(row, 1).text()
            bgt.limit = int(val)
        except ValueError:
            print(f"Unsupported limit format: '{val}'")
            bgt.limit = 0
            restore = True

        bgt.pk = self.row2pk[row]
        self.bgt_presenter.update(bgt, restore)
