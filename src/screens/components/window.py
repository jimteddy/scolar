from PySide6 import QtWidgets, QtGui, QtCore


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 200)
        self.setMaximumSize(600, 200)
        self.setStyleSheet(""" background-color: #3a7bff; color: #000; """)
        self.setup_ui()
        self.setup_data()

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def setup_data(self):
        self.table.setItem(0, 0, QtWidgets.QTableWidgetItem("1"))
        self.table.setItem(0, 1, QtWidgets.QTableWidgetItem("jimik"))
        self.table.setItem(0, 2, QtWidgets.QTableWidgetItem("jr.ikounga@gmail.com"))
        self.table.setItem(0, 3, QtWidgets.QTableWidgetItem("MASCULIN"))
        self.table.setItem(0, 4, QtWidgets.QTableWidgetItem("06 rue biamambou MADIBOU"))

    def create_widgets(self):
        self.table = QtWidgets.QTableWidget()
        self.table.setRowCount(3)
        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels(["MATRICULE", "NOM(S)", "PRENOM(S)", "SEXE", "ADRESSE"])
        #self.table.setVerticalHeaderLabels(["a", "b"])

    def modify_widgets(self):
        pass

    def create_layouts(self):
        self.layout_main = QtWidgets.QHBoxLayout()
        self.layout_main.addWidget(self.table)

    def add_widgets_to_layouts(self):
        self.setLayout(self.layout_main)

    def setup_connections(self):
        pass
