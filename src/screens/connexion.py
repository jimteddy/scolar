from PySide6 import QtWidgets, QtGui, QtCore
from hashlib import sha512

from src.screens.main import Main


class Popup(QtWidgets.QWidget):
    def __init__(self, titre, text):
        super().__init__()
        self.setWindowTitle(titre)
        self.lb_text = QtWidgets.QLabel(text)
        self.layout_main = QtWidgets.QVBoxLayout()
        self.layout_main.addWidget(self.lb_text)
        self.setLayout(self.layout_main)


class Connexion(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CONNEXION")
        self.isModal()
        self.isTopLevel()
        self.setMaximumSize(420, 260)
        self.setMinimumSize(420, 260)
        self.setStyleSheet(""" background-color: #3a7bff; color: #000; """)
        self.setup_ui()

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.lb_connecte = QtWidgets.QLabel("FORMULAIRE DE CONNEXION")
        self.lb_identifiant = QtWidgets.QLabel("Identifiant : ")
        self.le_identifiant = QtWidgets.QLineEdit()
        self.lb_password = QtWidgets.QLabel("Mot de passe : ")
        self.le_password = QtWidgets.QLineEdit()
        self.btn_submit = QtWidgets.QPushButton("Se connecter")

    def modify_widgets(self):
        self.lb_connecte.setFixedHeight(20)
        self.lb_connecte.setFont(QtGui.QFont('Times', 18))
        self.lb_connecte.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lb_connecte.setStyleSheet("""
            color: white;
        """)

        self.lb_identifiant.setFixedHeight(30)
        self.lb_identifiant.setFont(QtGui.QFont('Times', 14))

        self.le_identifiant.setPlaceholderText("Identitiant")
        self.le_identifiant.setFixedHeight(30)
        self.le_identifiant.setFont(QtGui.QFont('Times', 13))
        self.le_identifiant.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.le_password.setPlaceholderText("Mot de passe")
        self.le_password.setFixedHeight(30)
        self.le_password.setFont(QtGui.QFont('Times', 13))
        self.le_password.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.lb_password.setFixedHeight(30)
        self.lb_password.setFont(QtGui.QFont('Times', 14))

        self.btn_submit.setFont(QtGui.QFont('Times', 14))

    def create_layouts(self):
        self.formulaire = QtWidgets.QFormLayout()
        self.main_layout = QtWidgets.QVBoxLayout()
        self.unforget_layout = QtWidgets.QHBoxLayout()

    def add_widgets_to_layouts(self):
        self.formulaire.addRow(self.lb_identifiant, self.le_identifiant)
        self.formulaire.addRow(self.lb_password, self.le_password)
        self.formulaire.addWidget(self.btn_submit)

        self.main_layout.addWidget(self.lb_connecte)
        self.main_layout.addSpacing(50)
        self.main_layout.addLayout(self.formulaire)
        self.setLayout(self.main_layout)

    def setup_connections(self):
        self.btn_submit.clicked.connect(self.connexion)

    def connexion(self):
        if len(self.le_identifiant.text()) < 4:
            QtWidgets.QMessageBox.information(self, "Information",
                                              "Veuiller mentionner un identifiant")
        elif self.le_identifiant.text() != "admin":
            QtWidgets.QMessageBox.information(self, "Information",
                                              "Identifiant incorrect")
        else:
            if len(self.le_password.text()) < 7:
                QtWidgets.QMessageBox.information(self, "Information",
                                                  "veuiller mentionner un mot de passe de plus 8 caractères")
            elif self.le_password.text() != 'coucou123':
                QtWidgets.QMessageBox.information(self, "Information",
                                                  "Mot de passe incorrect")
            else:
                QtWidgets.QMessageBox.information(self, "Succes",
                                                  "Information correct")
