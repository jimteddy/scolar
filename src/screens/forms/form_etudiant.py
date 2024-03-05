from PySide6 import QtWidgets, QtGui, QtCore


def btn_action(text):
    btn = QtWidgets.QPushButton(text)
    btn.setFont(QtGui.QFont('Times', 14))
    btn.setFixedSize(180, 30)
    return btn


class FormEtudiant(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(QtCore.QSize(400, 300))
        self.setMaximumSize(QtCore.QSize(400, 300))
        self.setup_ui()

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        # self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connexion()

    def setup_data(self):pass

    def create_widgets(self):
        self.lb_matricule = QtWidgets.QLabel("MATRICULE")
        self.le_matricule = QtWidgets.QLineEdit()
        self.lb_nom = QtWidgets.QLabel("NOM(S)")
        self.le_nom = QtWidgets.QLineEdit()
        self.lb_prenom = QtWidgets.QLabel("PRENOM(S)")
        self.le_prenom = QtWidgets.QLineEdit()
        self.lb_sexe = QtWidgets.QLabel("SEXE : ")
        self.cb_sexe = QtWidgets.QComboBox()
        self.cb_sexe.addItems(["MASCULIN", "FEMININ"])
        self.btn_save = btn_action("Enregistrer")
        self.btn_set = btn_action("Modifier")
        self.btn_del = btn_action("Supprimer")

    def modify_widgets(self):
        # matricule
        self.lb_matricule.setFont(QtGui.QFont('Times', 14))
        self.lb_matricule.setFixedSize(110, 30)

        self.le_matricule.setFont(QtGui.QFont('Times', 14))
        # self.le_matricule.setPlaceholderText("Matricule")
        self.le_matricule.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.le_matricule.setFixedSize(180, 30)

        # nom
        self.lb_nom.setFont(QtGui.QFont('Times', 14))
        self.lb_nom.setFixedSize(110, 30)

        self.le_nom.setFont(QtGui.QFont('Times', 14))
        # self.le_nom.setPlaceholderText("Noms")
        self.le_nom.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.le_nom.setFixedHeight(30)

        # prenom
        self.lb_prenom.setFont(QtGui.QFont('Times', 14))
        # self.lb_prenom.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.lb_prenom.setFixedSize(110, 30)

        self.le_prenom.setFont(QtGui.QFont('Times', 14))
        # self.le_prenom.setPlaceholderText("Prenoms")
        self.le_prenom.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.le_prenom.setFixedHeight(30)

        # sexe
        self.lb_sexe.setFont(QtGui.QFont('Times', 14))
        self.lb_sexe.setFixedSize(110, 30)
        self.cb_sexe.setFont(QtGui.QFont('Times', 13))
        self.cb_sexe.setFixedSize(180, 30)

        self.btn_save.setStyleSheet("""
               background-color: green;
               """)
        self.btn_set.setStyleSheet("""
               background-color: orange;
               """)
        self.btn_del.setStyleSheet("""
               background-color: red;
               """)

    def add_widgets_to_layouts(self):
        self.formulaire = QtWidgets.QFormLayout()
        self.formulaire.addRow(self.lb_matricule, self.le_matricule)
        self.formulaire.addRow(self.lb_nom, self.le_nom)
        self.formulaire.addRow(self.lb_prenom, self.le_prenom)
        self.formulaire.addRow(self.lb_sexe, self.cb_sexe)
        self.formulaire.addWidget(self.btn_save)
        self.formulaire.addWidget(self.btn_set)
        self.formulaire.addWidget(self.btn_del)

        self.setLayout(self.formulaire)

    def setup_connexion(self):
        self.btn_save.clicked.connect(self.action_save)
        self.btn_set.clicked.connect(self.action_set)
        self.btn_del.clicked.connect(self.action_del)

    def action_save(self):
        print(self.le_matricule.text())
        print(self.le_nom.text())
        print(self.le_prenom.text())
        print(self.cb_sexe.currentText())

    def action_set(self):
        print("setter")

    def action_del(self):
        self.le_matricule.clear()
        self.le_nom.clear()
        self.le_prenom.clear()
