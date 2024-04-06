from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt, Slot

from bookkeeper.models.budget import Budget

from bookkeeper.view.abstract_budget_view import AbstractBudgetView

from bookkeeper.presenters.budget_presenter import BudgetPresenter


class BudgetView(AbstractBudgetView):
    def __init__(self):
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
        return self.vbox_layout
        

    def add(self, bgt: Budget) -> None:
        if bgt.pk == 0:
            raise ValueError('Trying to show object with empty `pk`')

        self.row2pk.insert(0, bgt.pk)
        self.table.blockSignals(True)
        self.table.insertRow(0)
        self.table.setVerticalHeaderItem(0, QtWidgets.QTableWidgetItem(bgt.period))
        amount_item = QtWidgets.QTableWidgetItem(str(bgt.amount))
        amount_item.setFlags(Qt.ItemIsEnabled)
        self.table.setItem(0, 0, amount_item)
        self.table.setItem(0, 1, QtWidgets.QTableWidgetItem(str(bgt.limit)))
        self.table.blockSignals(False)


    def update(self, bgt: Budget) -> None:
        try:
            row = self.row2pk.index(bgt.pk)
        except:
            raise ValueError('Trying to update budget unfamiliar to view')

        self.table.blockSignals(True)
        self.table.setVerticalHeaderItem(row, QtWidgets.QTableWidgetItem(bgt.period))
        item = self.table.item(row, 0)
        item.setText(str(bgt.amount))
        item.setData(Qt.BackgroundRole, None)
        item = self.table.item(row, 1)
        item.setText(str(bgt.limit))
        item.setData(Qt.BackgroundRole, None)
        self.table.blockSignals(False)


    def handle_exceeding(self, bgts: list[Budget]) -> None:
        self.table.blockSignals(True)
        for bgt in bgts:
            try:
                row = self.row2pk.index(bgt.pk)
            except:
                raise ValueError('Trying to handle exceeding budget unfamiliar to view')

            self.table.item(row, 0).setBackground(self.exceeding_brush)
            self.table.item(row, 1).setBackground(self.exceeding_brush)
        self.table.blockSignals(False)

        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle("Budget warning")
        periods = [bgt.period for bgt in bgts]
        msg_box.setText("Budget was exceeded for " + ", ".join(periods))
        msg_box.exec()


    @Slot()
    def on_table_cell_changed(self, row: int, column: int) -> None:
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
        except:
            print(f"Unsupported limit format: '{val}'")
            bgt.limit = None
            restore = True

        bgt.pk = self.row2pk[row]
        self.bgt_presenter.update(bgt, restore)
