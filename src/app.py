from PySide6 import QtWidgets
from package.main_window import MainWindow


def main():
    """fonction principale"""
    app = QtWidgets.QApplication()
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
