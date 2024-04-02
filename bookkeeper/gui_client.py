import sys
from PySide6.QtWidgets import QApplication

from bookkeeper.view.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

# from PySide6 import QtWidgets
# from PySide6.QtCore import Qt

# app = QtWidgets.QApplication(sys.argv)

# window.show()
# sys.exit(app.exec())