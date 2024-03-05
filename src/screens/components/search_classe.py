from PySide6 import QtWidgets, QtGui, QtCore


class FormSearchClasse(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setup_widget()
        self.setup_connexion()
        self.cb_classe.addItems(["Lic 1", "Lic 2", "Lic 3 GL", "Lic 3 SR"])

    def setup_widget(self):
        self.lb_classe = QtWidgets.QLabel("CLASSE")
        self.lb_classe.setFont(QtGui.QFont('Times', 14))
        self.lb_classe.setFixedSize(120, 30)
        self.lb_classe.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.cb_classe = QtWidgets.QComboBox()
        self.cb_classe.setFont(QtGui.QFont('Times', 13))
        self.cb_classe.setFixedSize(300, 30)

        self.formulaire = QtWidgets.QFormLayout()
        self.formulaire.addRow(self.lb_classe, self.cb_classe)

        self.setLayout(self.formulaire)

    def setup_connexion(self):
        self.cb_classe.currentTextChanged.connect(self.classe_changed)

    def classe_changed(self, cl):
        print(cl)