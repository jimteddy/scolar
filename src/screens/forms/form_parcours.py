from PySide6 import QtWidgets, QtGui, QtCore


class FormParcours(QtWidgets.QWidget):
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
        self.lb_parcours = QtWidgets.QLabel('Parcours : ')
        self.cb_parcours = QtWidgets.QComboBox()
        self.btn_parcours = QtWidgets.QPushButton('Ajouter un parcours')

    def modify_widgets(self):
        self.lb_parcours.setFont(QtGui.QFont('Times', 13))
        self.lb_parcours.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lb_parcours.setFixedHeight(30)

        self.cb_parcours.setFont(QtGui.QFont('Times', 13))
        self.cb_parcours.setFixedHeight(30)
        self.cb_parcours.setFixedWidth(150)

    def create_layouts(self):
        self.formulaire = QtWidgets.QFormLayout()
        self.layout_main = QtWidgets.QHBoxLayout()

    def add_widgets_to_layouts(self):
        self.formulaire.addRow(self.lb_parcours, self.cb_parcours)
        self.layout_main.addLayout(self.formulaire)
        self.layout_main.addWidget(self.btn_parcours)
        self.setLayout(self.layout_main)

    def setup_connections(self):
        self.btn_parcours.clicked.connect(self.add_parcours)

    def add_parcours(self):
        title, resultat = QtWidgets.QInputDialog.getText(self, "Ajouter un parcours", "Nom du parcours : ")
        if resultat and title:
            self.cb_parcours.addItem(title)


