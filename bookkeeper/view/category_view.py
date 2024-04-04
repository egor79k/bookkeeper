from PySide6 import QtWidgets
from PySide6.QtCore import Slot, Signal

from bookkeeper.models.category import Category

from bookkeeper.view.abstract_category_view import AbstractCategoryView

from bookkeeper.presenters.category_presenter import CategoryPresenter


class CategoryView(AbstractCategoryView):
    # Define signals
    # category_added = Signal(Category)
    # category_deleted = Signal(Category)


    def __init__(self):
        self.row2pk = []

        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.vbox_layout.addWidget(QtWidgets.QLabel('Categories'))

        self.tree = QtWidgets.QTreeWidget()
        self.vbox_layout.addWidget(self.tree)
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels(["Name"])

        items = QtWidgets.QTreeWidgetItem()
        items.setText(0, "Parent")
        # items.addChild(QtWidgets.QTreeWidgetItem())
        # items.child(0).setText(0, "Child")
        self.tree.insertTopLevelItems(0, [items])

        form_layout = QtWidgets.QFormLayout()
        self.vbox_layout.addLayout(form_layout)
        self.name_input = QtWidgets.QLineEdit()
        # self.parent_input = QtWidgets.QComboBox()
        self.delete_button = QtWidgets.QPushButton('Delete')
        self.add_button = QtWidgets.QPushButton('Add')
        form_layout.addRow(QtWidgets.QLabel('Name'), self.name_input)
        # form_layout.addRow(QtWidgets.QLabel('Parent'), self.parent_input)
        form_layout.addRow(self.delete_button, self.add_button)

        # Connect slots to signals
        self.add_button.clicked.connect(self.on_add_button_clicked)
        self.delete_button.clicked.connect(self.on_delete_button_clicked)


    def get_layout(self) -> QtWidgets.QLayout:
        return self.vbox_layout


    def add_category(self, cat: Category) -> None:
        pass


    def update_all(self, cats: list[Category]) -> None:
        pass


    def show_category(self, cat: Category) -> None:
        if cat.pk == 0:
            raise ValueError('Trying to show object with empty `pk`')

        self.row2pk.append(cat.pk)
        item = QtWidgets.QTreeWidgetItem()
        item.setText(0, cat.name)
        self.tree.addTopLevelItem(item)


    @Slot()
    def on_add_button_clicked(self) -> None:
        print('Add button clicked')
        name = self.name_input.text()
        self.name_input.clear()
        cat = Category(name)

        self.category_presenter.add(cat) # NOT IMPLEMENTED

        self.show_category(cat)

        self.category_added.emit(cat)
        
        
    @Slot()
    def on_delete_button_clicked(self) -> None:
        print('Delete button clicked')
        