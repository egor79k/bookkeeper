""" Contains class implementing the GUI for categories list """

from PySide6 import QtWidgets, QtCore

from bookkeeper.models.category import Category

from bookkeeper.view.abstract_category_view import AbstractCategoryView


class CategoryView(AbstractCategoryView):
    """
    This class implements a GUI for categories list, allowing user
    to create, list, update and delete categories from database.
    It is a part of MVP architecture so it handles link to category presenter.
    Therefore set_presenter() method of abstract base class must be called
    before calling any other methods.
    All user actions are passed to presenter and don't cause any changes
    in UI directly. Presenter calls back to this view to display changes
    in UI after doing necessary logic.
    Categories list is stored in the tree widget to provide a future support
    for subcategories which is not implemented yet.

    Attributes:
        row2pk - list matching category's row in tree to it's pk in database
    """

    row2pk: list[int]

    def __init__(self) -> None:
        self.row2pk = []

        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.vbox_layout.addWidget(QtWidgets.QLabel('Categories'))

        self.tree = QtWidgets.QTreeWidget()
        self.vbox_layout.addWidget(self.tree)
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels(["Name"])

        self.current_editable_item = QtWidgets.QTreeWidgetItem()
        form_layout = QtWidgets.QFormLayout()
        self.vbox_layout.addLayout(form_layout)
        self.edit_name_input = QtWidgets.QLineEdit()
        self.edit_name_input.setEnabled(False)
        self.name_input = QtWidgets.QLineEdit()
        delete_button = QtWidgets.QPushButton('Delete')
        add_button = QtWidgets.QPushButton('Add')
        form_layout.addRow(QtWidgets.QLabel('Edit'), self.edit_name_input)
        form_layout.addRow(QtWidgets.QLabel('Name'), self.name_input)
        form_layout.addRow(delete_button, add_button)

        # Connect slots to signals
        self.tree.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.edit_name_input.returnPressed.connect(self.on_edit_name_input_return_pressed)
        add_button.clicked.connect(self.on_add_button_clicked)
        delete_button.clicked.connect(self.on_delete_button_clicked)

    def get_layout(self) -> QtWidgets.QLayout:
        """
        Get layout to insert categories widgets into window

        Returns:
            QLayout object containing category UI
        """
        return self.vbox_layout

    def add(self, cat: Category) -> None:
        """
        Adds new category to view. Creates new item in categories tree.

        Parameters:
            cat - Category object from database
        """
        if cat.pk == 0:
            raise ValueError('Trying to show object with empty `pk`')

        self.row2pk.append(cat.pk)
        item = QtWidgets.QTreeWidgetItem()
        item.setText(0, cat.name)
        self.tree.addTopLevelItem(item)

    def update(self, cat: Category) -> None:
        """
        Updates an existing category data in the tree.

        Parameters:
            cat - Category object from database
        """
        self.current_editable_item.setText(0, cat.name)

    def delete(self, pk: int) -> None:
        """
        Deletes category from tree view.

        Parameters:
            pk - id of Category object in database (primary key)
        """
        row = self.row2pk.index(pk)
        self.row2pk.pop(row)
        self.tree.takeTopLevelItem(row)

    def warning(self, msg: str) -> None:
        """
        Informs user about something with pop-up window.
        For example, used when trying to delete category with existing expenses.

        Parameters:
            msg - message string
        """
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle("Category warning")
        msg_box.setText(msg)
        msg_box.exec()

    @QtCore.Slot()
    def on_item_double_clicked(self,
                               item: QtWidgets.QTreeWidgetItem,
                               column: int) -> None:
        """
        Handles start of editing category on double click.

        Parameters:
            item   - tree item being modified
            column - column of item being modified (only one now)
        """
        self.edit_name_input.setEnabled(True)
        self.edit_name_input.setText(item.text(column))
        self.current_editable_item = item

    @QtCore.Slot()
    def on_edit_name_input_return_pressed(self) -> None:
        """
        Handles finish of editing category on pressing enter in the edit line.
        """
        new_name = self.edit_name_input.text()
        self.edit_name_input.clear()
        self.edit_name_input.setEnabled(False)
        row = self.tree.indexOfTopLevelItem(self.current_editable_item)
        pk = self.row2pk[row]
        self.cat_presenter.update(Category(name=new_name, parent=None, pk=pk))

    @QtCore.Slot()
    def on_add_button_clicked(self) -> None:
        """
        Handles click on add button passing new category to presenter.
        Does not change view. All changes in UI are caused by the presenter.
        """
        name = self.name_input.text()
        self.name_input.clear()
        cat = Category(name)
        self.cat_presenter.add(cat)

    @QtCore.Slot()
    def on_delete_button_clicked(self) -> None:
        """
        Handles click on delete button passing pk of the category being deleted
        to the presenter.
        Does not change view. All changes in UI are caused by the presenter.
        """
        items = self.tree.selectedItems()
        if len(items) == 0:
            return

        row = self.tree.indexOfTopLevelItem(items[0])
        pk = self.row2pk[row]
        self.cat_presenter.delete(pk)
