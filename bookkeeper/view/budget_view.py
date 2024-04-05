from PySide6 import QtWidgets

from bookkeeper.models.budget import Budget

from bookkeeper.view.abstract_budget_view import AbstractBudgetView

from bookkeeper.presenters.budget_presenter import BudgetPresenter


class BudgetView(AbstractBudgetView):
    def __init__(self):
        self.row2pk = []

        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.vbox_layout.addWidget(QtWidgets.QLabel('Budget'))

        self.table = QtWidgets.QTableWidget(3, 2)
        self.vbox_layout.addWidget(self.table, 4)
        # self.table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table.setHorizontalHeaderLabels("Summ Budget".split())
        self.table.setVerticalHeaderLabels("Day Week Month".split())
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)


    def get_layout(self) -> QtWidgets.QLayout:
        return self.vbox_layout
        

    def add(self, bgt: Budget) -> None:
        if bgt.pk == 0:
            raise ValueError('Trying to show object with empty `pk`')

        self.row2pk.insert(0, bgt.pk)
        self.table.insertRow(0)
        # self.table.setItem(0, 0, QtWidgets.QTableWidgetItem(exp.expense_date.strftime('%Y-%m-%d %H:%M')))
        # self.table.setItem(0, 1, QtWidgets.QTableWidgetItem(str(exp.amount)))
        # cat_item = QtWidgets.QTableWidgetItem(cat_name)
        # cat_item.setFlags(Qt.ItemIsEnabled)
        # self.table.setItem(0, 2, cat_item)
        # self.table.setItem(0, 3, QtWidgets.QTableWidgetItem(exp.comment))
