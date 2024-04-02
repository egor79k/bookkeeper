from PySide6 import QtWidgets
from bookkeeper.presenters.budget_presenter import BudgetPresenter


class BudgetView(QtWidgets.QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.presenter = BudgetPresenter()
        
        super().addWidget(QtWidgets.QLabel('Budget'))

        budget_table = QtWidgets.QTableWidget(3, 2)
        super().addWidget(budget_table, 4)
        # budget_table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        budget_table.setHorizontalHeaderLabels("Summ Budget".split())
        budget_table.setVerticalHeaderLabels("Day Week Month".split())
        header = budget_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        

    # def on_add_budget_button_click(self):
    #     exp = Expense()
    #     # presenter.addExpense(exp)
