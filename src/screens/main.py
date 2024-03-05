from PySide6 import QtWidgets, QtGui

from src.package.api2.etudiant import Etudiant
from src.screens.forms.form_etudiant import FormEtudiant
from src.screens.components.search_classe import FormSearchClasse
from src.screens.components.table_etudiant import TableEtudiant


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SCOLAR")
        self.setWindowIcon(QtGui.QIcon("../resources/icons/Icon.ico"))
        self.setMinimumSize(self.taille[0], self.taille[1])
        self.setGeometry(70, 50, 0, 0)
        self.setStyleSheet(""" background-color: #3a7cff; color: #000; """)

        self.liste_etudiant: [Etudiant] = Etudiant.create_liste()
        self.setup_ui()
        self.setup_data()

    @property
    def taille(self):
        return 1200, 700

    def setup_ui(self):
        # self.setCentralWidget(Window())
        # self.menubarre()
        self.create_widgets()
        self.modify_widgets()
        self.setup_layouts()
        self.setup_connections()

    def setup_data(self):
        pass

    def menubarre(self):
        self.menuBarre = self.menuBar()

        self.file = self.menuBarre.addMenu("Fichier")
        self.file1 = QtGui.QAction("Fichier1", self)
        self.file2 = QtGui.QAction("Fichier2", self)
        self.file.addActions([self.file1, self.file2])

        self.classe = QtGui.QAction("Classe", self)
        self.salle = QtGui.QAction("Salle", self)
        self.examen = QtGui.QAction("Examen", self)
        self.parametre = QtGui.QAction("Paramêtre", self)

        self.menuBarre.addActions([self.classe, self.salle, self.examen, self.parametre])

        self.file.triggered.connect(self.menu_bar_exec)
        self.menuBarre.triggered.connect(self.menu_bar_exec)

    def create_widgets(self):
        self.formEtudiant = FormEtudiant()
        self.formSearchClasse = FormSearchClasse()
        self.tableEtudiant = TableEtudiant(liste=self.liste_etudiant)

    def modify_widgets(self):pass

    def setup_layouts(self):
        self.widget_left = QtWidgets.QWidget()
        self.widget_left.setFixedWidth(420)
        self.widget_left.setStyleSheet("""
            background-color: #ccc;
        """)
        self.layout_left = QtWidgets.QVBoxLayout()
        self.layout_left.setContentsMargins(0, 0, 0, 0)
        self.layout_left.addWidget(self.formEtudiant)
        self.layout_left.addStretch()
        self.widget_left.setLayout(self.layout_left)

        self.widget_right = QtWidgets.QWidget()
        self.widget_right.setStyleSheet("""
            background-color: #aaa;
        """)
        self.layout_right = QtWidgets.QVBoxLayout()
        self.layout_right.setContentsMargins(0, 0, 0, 0)
        self.layout_right.addWidget(self.formSearchClasse)
        self.layout_right.addWidget(self.tableEtudiant)
        self.layout_right.addStretch()
        self.widget_right.setLayout(self.layout_right)

        self.layout_main = QtWidgets.QHBoxLayout()
        self.layout_main.addWidget(self.widget_left)
        self.layout_main.addWidget(self.widget_right)

        widget = QtWidgets.QWidget()
        widget.setLayout(self.layout_main)
        self.setCentralWidget(widget)

    def setup_connections(self): pass

    def menu_bar_exec(self, param):
        if param.text() == "Fichier":
            print(param.text())
        if param.text() == "Classe":
            print(param.text())
        if param.text() == "Salle":
            print(param.text())
        if param.text() == "Examen":
            print(param.text())
        if param.text() == "Paramêtre":
            print(param.text())


