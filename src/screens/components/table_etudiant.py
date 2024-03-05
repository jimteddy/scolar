from PySide6 import QtWidgets, QtGui, QtCore

from src.package.api2.etudiant import Etudiant


class TableEtudiant(QtWidgets.QWidget):
    def __init__(self, liste = []):
        super().__init__()
        self.setMinimumWidth(350)
        self.setMaximumWidth(350)
        self.liste: [Etudiant] = liste
        self.setup_ui()
        self.setup_data()
        
    def setup_ui(self):
        self.setup_widget()
        self.setup_connexion()
        
    def setup_widget(self): 
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Noms", "Prenoms"])
        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 150)

        # self.table.setSelectMode(QtWidgets.QAbstractItemView.NoSelect)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        self.layout_table = QtWidgets.QHBoxLayout()
        self.layout_table.addWidget(self.table)
        self.setLayout(self.layout_table)
    
    def setup_data(self): pass
        #self.table.setRowCount(len(self.liste))
    
    def setup_connexion(self): pass
    