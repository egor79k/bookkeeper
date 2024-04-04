from PySide6 import QtWidgets

from bookkeeper.models.budget import Budget

from bookkeeper.view.abstract_budget_view import AbstractBudgetView

from bookkeeper.presenters.budget_presenter import BudgetPresenter


class BudgetView(AbstractBudgetView):
    def __init__(self):

        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.vbox_layout.addWidget(QtWidgets.QLabel('Budget'))

        budget_table = QtWidgets.QTableWidget(3, 2)
        self.vbox_layout.addWidget(budget_table, 4)
        # budget_table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        budget_table.setHorizontalHeaderLabels("Summ Budget".split())
        budget_table.setVerticalHeaderLabels("Day Week Month".split())
        header = budget_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)


    def get_layout(self) -> QtWidgets.QLayout:
        return self.vbox_layout
        

    def add_budget(self, bgt: Budget) -> None:
        pass


    def update_all(self, bgts: list[Budget]) -> None:
        pass
