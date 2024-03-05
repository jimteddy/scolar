from PySide6 import QtWidgets, QtGui, QtCore


class FormMatiere(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 50)
        self.setMaximumSize(400, 50)
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
        pass

    def create_widgets(self):
        self.lb_matiere = QtWidgets.QLabel('Matière : ')
        self.cb_matiere = QtWidgets.QComboBox()
        self.btn_matiere = QtWidgets.QPushButton('Ajouter une Matière')

        self.le_matiere = QtWidgets.QLineEdit()

    def modify_widgets(self):
        self.lb_matiere.setFont(QtGui.QFont('Times', 13))
        self.lb_matiere.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lb_matiere.setFixedHeight(30)

        self.cb_matiere.setFont(QtGui.QFont('Times', 13))
        self.cb_matiere.setFixedHeight(30)
        self.cb_matiere.setFixedWidth(150)

    def create_layouts(self):
        self.formulaire = QtWidgets.QFormLayout()
        self.layout_main = QtWidgets.QHBoxLayout()

    def add_widgets_to_layouts(self):
        self.formulaire.addRow(self.lb_matiere, self.cb_matiere)
        self.layout_main.addLayout(self.formulaire)
        self.layout_main.addWidget(self.btn_matiere)
        self.setLayout(self.layout_main)

    def setup_connections(self):
        self.btn_matiere.clicked.connect(self.add_matiere)

    def add_matiere(self):
        title, resultat = QtWidgets.QInputDialog.getText(self, "Ajouter une matière", "Nom de la matière : ")
        if resultat and title:
            self.cb_matiere.addItem(title)


