from PySide6 import QtWidgets
from PySide6.QtCore import Qt, Slot

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

        self.current_editable_item = None
        form_layout = QtWidgets.QFormLayout()
        self.vbox_layout.addLayout(form_layout)
        self.edit_name_input = QtWidgets.QLineEdit()
        self.edit_name_input.setEnabled(False)
        self.name_input = QtWidgets.QLineEdit()
        # self.parent_input = QtWidgets.QComboBox()
        self.delete_button = QtWidgets.QPushButton('Delete')
        self.add_button = QtWidgets.QPushButton('Add')
        form_layout.addRow(QtWidgets.QLabel('Edit'), self.edit_name_input)
        form_layout.addRow(QtWidgets.QLabel('Name'), self.name_input)
        # form_layout.addRow(QtWidgets.QLabel('Parent'), self.parent_input)
        form_layout.addRow(self.delete_button, self.add_button)

        # Connect slots to signals
        self.tree.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.edit_name_input.returnPressed.connect(self.on_edit_name_input_return_pressed)
        self.add_button.clicked.connect(self.on_add_button_clicked)
        self.delete_button.clicked.connect(self.on_delete_button_clicked)

        # TEMP
        # items = QtWidgets.QTreeWidgetItem()
        # items.setText(0, "Parent")
        # # items.addChild(QtWidgets.QTreeWidgetItem())
        # # items.child(0).setText(0, "Child")
        # self.tree.insertTopLevelItems(0, [items])


    def set_presenter(self, cat_presenter: CategoryPresenter) -> None:
        self.cat_presenter = cat_presenter

        # Connect ...


    def get_layout(self) -> QtWidgets.QLayout:
        return self.vbox_layout


    def add(self, cat: Category) -> None:
        if cat.pk == 0:
            raise ValueError('Trying to show object with empty `pk`')

        self.row2pk.append(cat.pk)
        item = QtWidgets.QTreeWidgetItem()
        # item.setFlags(Qt.ItemIsEnabled)
        item.setText(0, cat.name)
        self.tree.addTopLevelItem(item)


    def update(self, cat: Category) -> None:
        self.current_editable_item.setText(0, cat.name)


    def delete(self, pk: int) -> None:
        row = self.row2pk.index(pk)
        self.row2pk.pop(row)
        self.tree.takeTopLevelItem(row)


    def update_all(self, cats: list[Category]) -> None:
        pass


    def show_category(self, cat: Category) -> None:
        pass


    @Slot()
    def on_item_double_clicked(self, item: QtWidgets.QTreeWidgetItem, column: int):
        self.edit_name_input.setEnabled(True)
        self.edit_name_input.setText(item.text(0))
        self.current_editable_item = item


    @Slot()
    def on_edit_name_input_return_pressed(self) -> None:
        new_name = self.edit_name_input.text()
        self.edit_name_input.clear()
        self.edit_name_input.setEnabled(False)
        row = self.tree.indexOfTopLevelItem(self.current_editable_item)
        pk = self.row2pk[row]
        self.cat_presenter.update(Category(name=new_name, parent=None, pk=pk))


    @Slot()
    def on_add_button_clicked(self) -> None:
        name = self.name_input.text()
        self.name_input.clear()
        cat = Category(name)
        self.cat_presenter.add(cat)

        
    @Slot()
    def on_delete_button_clicked(self) -> None:
        row = self.tree.indexOfTopLevelItem(self.tree.selectedItems()[0])
        pk = self.row2pk[row]
        self.cat_presenter.delete(pk)
        