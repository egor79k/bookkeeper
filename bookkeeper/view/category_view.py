from PySide6 import QtWidgets
from bookkeeper.presenters.category_presenter import CategoryPresenter


class CategoryView(QtWidgets.QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.presenter = CategoryPresenter()
        
        super().addWidget(QtWidgets.QLabel('Categories'))

        categories_tree = QtWidgets.QTreeWidget()
        super().addWidget(categories_tree)
        categories_tree.setColumnCount(1)
        categories_tree.setHeaderLabels(["Name"])

        items = QtWidgets.QTreeWidgetItem()
        items.setText(0, "Parent")
        items.addChild(QtWidgets.QTreeWidgetItem())
        items.child(0).setText(0, "Child")
        categories_tree.insertTopLevelItems(0, [items])

        form_layout = QtWidgets.QFormLayout()
        super().addLayout(form_layout)
        self.category_input = QtWidgets.QComboBox()
        self.delete_button = QtWidgets.QPushButton('Delete')
        self.add_button = QtWidgets.QPushButton('Add')
        form_layout.addRow(QtWidgets.QLabel('Parent'), self.category_input)
        form_layout.addRow(self.delete_button, self.add_button)


    # def on_add_expense_button_click(self):
    #     exp = Category()
    #     # presenter.addCategory(exp)
