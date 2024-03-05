from functools import partial
from PySide6 import QtWidgets, QtGui, QtCore, QtPrintSupport

from src.package.api.salle import get_salles, Salle, ImpressionSalle
from src.package.api.classe import get_classes, Classe
from src.package.api.repartition import Repartition
from .word import Word
from .item_area import ClasseItem, SalleItem
from .scrolllabel import ScrollLabel
from .worker import Worker, TrieThread


def get_selected_repartition_list(lw_liste_repartition):
    liste = []
    for i in range(lw_liste_repartition.count()):
        if lw_liste_repartition.item(i).select:
            liste.append(lw_liste_repartition.item(i))
    return liste


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Repartion des étudiants dans les salles")
        self.setWindowIcon(QtGui.QIcon("resources/icons/Icon.ico"))
        self.setFixedSize(720, 600)
        self.setup_ui()
        self.stack.setCurrentWidget(self.home_widget)
        self.setup_data()
        self.salles = []

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.add_action_to_toolbar()
        self.setup_connections()

    def setup_data(self):
        self.populate_salles()
        self.populate_classes()

    def create_widgets(self):
        #
        self.toolbar = QtWidgets.QToolBar()
        self.btn_gerer_salle = QtWidgets.QPushButton("Gestion des salles")
        self.btn_gerer_classe = QtWidgets.QPushButton("Gestion des classes")
        self.btn_gerer_repartition = QtWidgets.QPushButton("Répartition")
        self.btn_parametrage = QtWidgets.QPushButton("A propos du logiciel")

        # Pour la salle
        self.btn_create_salle = QtWidgets.QPushButton("Ajouter une salle")
        self.btn_create_salle.setFont(QtGui.QFont('Times', 11))
        self.btn_create_salle.setIcon(QtGui.QIcon("resources/apps-add.svg"))
        self.btn_create_salle.setIconSize(QtCore.QSize(30, 30))

        self.lw_salle = QtWidgets.QListWidget()
        self.label_libelle = QtWidgets.QLabel("Nom de salles :")
        self.le_libelle = QtWidgets.QLineEdit()
        self.label_limite = QtWidgets.QLabel("Nombre de places : ")
        self.sb_limite = QtWidgets.QSpinBox()
        self.label_table_banc = QtWidgets.QLabel("Nombre de table bancs : ")
        self.table_banc = QtWidgets.QLabel("0")

        self.btn_delete_salle = QtWidgets.QPushButton("Supprimer la salle")
        self.btn_delete_salle.setFont(QtGui.QFont('Times', 11))
        self.btn_delete_salle.setIcon(QtGui.QIcon("resources/apps-supprimer.svg"))
        self.btn_delete_salle.setIconSize(QtCore.QSize(30, 30))

        # pour la classe
        self.btn_create_classe = QtWidgets.QPushButton("Ajouter une classe")
        self.btn_create_classe.setFont(QtGui.QFont('Times', 12))
        self.btn_create_classe.setIcon(QtGui.QIcon("resources/utilisateurs-medicaux.svg"))
        self.btn_create_classe.setIconSize(QtCore.QSize(30, 30))

        self.btn_load_classe_word = QtWidgets.QPushButton("Charger le fichier")
        self.btn_load_classe_word.setFont(QtGui.QFont('Times', 11))
        self.btn_load_classe_word.setIcon(QtGui.QIcon("resources/telecharger-un-fichier.png"))
        self.btn_load_classe_word.setIconSize(QtCore.QSize(30, 30))

        self.lw_classe = QtWidgets.QListWidget()
        self.tw_classe = QtWidgets.QTableWidget()
        self.lb_drop = QtWidgets.QLabel("^Déposer le fichier dans l'interface")
        self.lb_select = QtWidgets.QLabel("^Sélectionner une classe")
        self.btn_delete_classe = QtWidgets.QPushButton("Supprimer la classe")
        self.btn_delete_classe.setFont(QtGui.QFont('Times', 12))
        self.btn_delete_classe.setIcon(QtGui.QIcon("resources/supprimer-lutilisateur.png"))
        self.btn_delete_classe.setIconSize(QtCore.QSize(30, 30))

        # pour la repartition
        self.btn_imprimer_pdf = QtWidgets.QPushButton("Apperçu en pdf")
        self.btn_imprimer_word = QtWidgets.QPushButton("Apperçu en word")
        self.btn_appercu = QtWidgets.QPushButton("Voir un apperçu")
        self.btn_trier = QtWidgets.QPushButton("Trier")
        self.cb_classe = QtWidgets.QCheckBox("Selectionner toutes les classes")
        self.cb_salle = QtWidgets.QCheckBox("Selectionner toutes les salles")
        self.lw_repartition_salle = QtWidgets.QListWidget()
        self.lw_repartition_classe = QtWidgets.QListWidget()

        self.label_effectif_total_classe_info = QtWidgets.QLabel("Effectif total d'etudiants: ")
        self.label_effectif_total_classe_info.setFont(QtGui.QFont('Times', 12))
        self.label_effectif_total_classe = QtWidgets.QLabel("0")
        self.label_effectif_total_classe.setFont(QtGui.QFont('Times', 13))
        self.label_effectif_total_salle_info = QtWidgets.QLabel("Nombre total de places: ")
        self.label_effectif_total_salle_info.setFont(QtGui.QFont('Times', 12))
        self.label_effectif_total_salle = QtWidgets.QLabel("0")
        self.label_effectif_total_salle.setFont(QtGui.QFont('Times', 13))
        # pour A propos

        # widgets principaux
        self.stack = QtWidgets.QStackedLayout()
        self.home_widget = QtWidgets.QWidget()
        self.classe_widget = QtWidgets.QWidget()
        self.salle_widget = QtWidgets.QWidget()
        self.repartition_widget = QtWidgets.QWidget()
        self.setting_widget = QtWidgets.QWidget()
        self.main_widget = QtWidgets.QWidget()

    def modify_widgets(self):
        css_file = "resources/Perstfic.qss"
        with open(css_file, "r") as f:
            self.setStyleSheet(f.read())

        self.setAcceptDrops(True)

        size = 260, 260

        self.cb_classe.setFont(QtGui.QFont('Times', 11))
        self.cb_salle.setFont(QtGui.QFont('Times', 11))

        self.btn_gerer_classe.setFixedSize(*size)
        self.btn_gerer_classe.setFont(QtGui.QFont('Times', 11))
        self.btn_gerer_classe.setIcon(QtGui.QIcon("resources/utilisateurs-alt.png"))
        self.btn_gerer_classe.setIconSize(QtCore.QSize(100, 100))

        self.btn_gerer_salle.setFixedSize(*size)
        self.btn_gerer_salle.setFont(QtGui.QFont('Times', 12))
        self.btn_gerer_salle.setIcon(QtGui.QIcon("resources/salle-de-classe.png"))
        self.btn_gerer_salle.setIconSize(QtCore.QSize(100, 100))

        self.btn_gerer_repartition.setFixedSize(*size)
        self.btn_gerer_repartition.setFont(QtGui.QFont('Times', 12))
        self.btn_gerer_repartition.setIcon(QtGui.QIcon("resources/repartition-des-taches.png"))
        self.btn_gerer_repartition.setIconSize(QtCore.QSize(100, 100))

        self.btn_parametrage.setFixedSize(*size)
        self.btn_parametrage.setFont(QtGui.QFont('Times', 11))
        self.btn_parametrage.setIcon(QtGui.QIcon("resources/reportage.png"))
        self.btn_parametrage.setIconSize(QtCore.QSize(100, 100))

        # pour l'onglet salle
        self.label_libelle.setFixedSize(100, 30)
        self.label_libelle.setFont(QtGui.QFont('Times', 12))

        self.le_libelle.setFixedSize(120, 30)
        self.le_libelle.setFont(QtGui.QFont('Times', 12))

        self.label_limite.setFixedSize(170, 30)
        self.label_limite.setFont(QtGui.QFont('Times', 12))

        self.label_table_banc.setFixedSize(190, 30)
        self.label_table_banc.setFont(QtGui.QFont('Times', 12))

        self.table_banc.setFixedSize(30, 30)
        self.table_banc.setFont(QtGui.QFont('Times', 12))

        self.sb_limite.setFixedSize(50, 30)
        self.sb_limite.setRange(0, 300)
        self.sb_limite.setFont(QtGui.QFont('Times', 12))

        # pour la classe
        self.tw_classe.setColumnCount(3)
        self.tw_classe.setHorizontalHeaderLabels(["Noms", "Prenoms", "Sexe"])
        self.tw_classe.setColumnWidth(0, 150)
        self.tw_classe.setColumnWidth(1, 150)
        self.tw_classe.setColumnWidth(2, 40)

        # self.tw_classe.setSelectMode(QtWidgets.QAbstractItemView.NoSelect)
        self.tw_classe.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.tw_classe.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        self.lb_drop.setVisible(False)
        self.lb_drop.setFont(QtGui.QFont('Times', 12))
        self.lb_select.setVisible(True)
        self.lb_select.setFont(QtGui.QFont('Times', 12))

        self.btn_appercu.setEnabled(False)
        self.btn_appercu.setFont(QtGui.QFont('Times', 11))

        self.btn_imprimer_pdf.setEnabled(False)
        self.btn_imprimer_pdf.setFont(QtGui.QFont('Times', 11))
        self.btn_imprimer_pdf.setIcon(QtGui.QIcon("resources/fichier-pdf.png"))

        self.btn_imprimer_word.setEnabled(False)
        self.btn_imprimer_word.setFont(QtGui.QFont('Times', 11))
        self.btn_imprimer_word.setIcon(QtGui.QIcon("resources/mot.png"))

        self.btn_trier.setIcon(QtGui.QIcon("resources/sorte.svg"))
        self.btn_trier.setFont(QtGui.QFont('Times', 11))

    def create_layouts(self):
        self.home_layout = QtWidgets.QGridLayout()
        self.classe_layout = QtWidgets.QGridLayout()
        self.salle_layout = QtWidgets.QGridLayout()
        self.repartition_layout = QtWidgets.QGridLayout()
        self.setting_layout = QtWidgets.QGridLayout()

        # for salle
        self.hbox_name = QtWidgets.QHBoxLayout()
        self.hbox_limite = QtWidgets.QHBoxLayout()
        self.hbox_banc = QtWidgets.QHBoxLayout()
        self.vbox = QtWidgets.QVBoxLayout()
        self.btn_list_salle = QtWidgets.QHBoxLayout()

        # classe
        self.btn_list_classe = QtWidgets.QHBoxLayout()

        # for repartition
        self.vbox_btn = QtWidgets.QVBoxLayout()
        self.vbox_classe = QtWidgets.QVBoxLayout()
        self.vbox_salle = QtWidgets.QVBoxLayout()
        self.hbox_left = QtWidgets.QHBoxLayout()
        self.hbox_right = QtWidgets.QHBoxLayout()

        # for settings

    def add_widgets_to_layouts(self):
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)

        self.home_layout.addWidget(self.btn_gerer_classe, 0, 0, 1, 1)
        self.home_layout.addWidget(self.btn_gerer_repartition, 0, 1, 1, 1)
        self.home_layout.addWidget(self.btn_gerer_salle, 1, 0, 1, 1)
        self.home_layout.addWidget(self.btn_parametrage, 1, 1, 1, 1)

        self.home_widget.setLayout(self.home_layout)
        self.stack.addWidget(self.home_widget)

        self.classe_widget.setLayout(self.classe_layout)
        self.stack.addWidget(self.classe_widget)

        self.salle_widget.setLayout(self.salle_layout)
        self.stack.addWidget(self.salle_widget)

        self.repartition_widget.setLayout(self.repartition_layout)
        self.stack.addWidget(self.repartition_widget)

        self.setting_widget.setLayout(self.setting_layout)
        self.stack.addWidget(self.setting_widget)

        self.main_widget.setLayout(self.stack)
        self.setCentralWidget(self.main_widget)

        # pour la salle
        self.hbox_name.addWidget(self.label_libelle)
        self.hbox_name.addWidget(self.le_libelle)
        self.vbox.addLayout(self.hbox_name)
        self.hbox_limite.addWidget(self.label_limite)
        self.hbox_limite.addWidget(self.sb_limite)
        self.hbox_banc.addWidget(self.label_table_banc)
        self.hbox_banc.addWidget(self.table_banc)
        self.vbox.addLayout(self.hbox_limite)
        self.vbox.addLayout(self.hbox_banc)
        self.btn_list_salle.addWidget(self.btn_create_salle)
        self.btn_list_salle.addWidget(self.btn_delete_salle)

        self.salle_layout.addLayout(self.btn_list_salle, 0, 0, 1, 1)
        self.salle_layout.addWidget(self.lw_salle, 1, 0, 1, 1)
        self.salle_layout.addLayout(self.vbox, 0, 2, 1, 1)

        # pour la classe
        self.btn_list_classe.addWidget(self.btn_create_classe)
        self.btn_list_classe.addWidget(self.btn_delete_classe)
        self.classe_layout.addLayout(self.btn_list_classe, 0, 0, 1, 1)
        self.classe_layout.addWidget(self.btn_load_classe_word, 0, 1, 1, 1)
        self.classe_layout.addWidget(self.lw_classe, 1, 0, 1, 1)
        self.classe_layout.addWidget(self.tw_classe, 1, 1, 1, 1)
        self.classe_layout.addWidget(self.lb_drop, 2, 1, 1, 1)
        self.classe_layout.addWidget(self.lb_select, 2, 0, 1, 1)

        # pour la repartition
        self.vbox_classe.addWidget(self.cb_classe)
        self.vbox_classe.addWidget(self.lw_repartition_classe)
        self.vbox_salle.addWidget(self.cb_salle)
        self.vbox_salle.addWidget(self.lw_repartition_salle)
        # self.vbox_btn.addWidget(self.btn_appercu)
        self.vbox_btn.addWidget(self.btn_imprimer_pdf)
        self.vbox_btn.addWidget(self.btn_imprimer_word)
        self.vbox_btn.addWidget(self.btn_trier)
        self.hbox_left.addWidget(self.label_effectif_total_salle_info)
        self.hbox_left.addWidget(self.label_effectif_total_salle)
        self.hbox_right.addWidget(self.label_effectif_total_classe_info)
        self.hbox_right.addWidget(self.label_effectif_total_classe)
        self.vbox_classe.addLayout(self.hbox_right)
        self.vbox_salle.addLayout(self.hbox_left)
        self.repartition_layout.addLayout(self.vbox_btn, 0, 0, 1, 1)
        self.repartition_layout.addLayout(self.vbox_salle, 0, 1, 1, 1)
        self.repartition_layout.addLayout(self.vbox_classe, 0, 2, 1, 1)

        # setting
        self.label = ScrollLabel()
        self.label.setText(
            """Comment utiliser le logiciel: \n
            1- Définir les salles: aller sur gestion des salles ou Salle sur la bar d'outil.\n
             1.1- Pour créer une salle: cliquer sur ajouter salle puis renseigner le nom de la salle\n
             1.2- Pour definir le nombre limite d'élèves dans une salle: renseigner l'effectif dans le champs nombre de places \n
             1.3- Le nombre de table banc est générer automatiquement pour une cohérence pendant le trie des élèves dans les salles.\n
             1.4- Lors de la la création, ou la modification, les informations sont enregistrer automatiquement.\n 
            2: Définir les classes:\n
             2.1- Pour créer une classe: cliquer sur ajouter une classe puis renseigner le nom de la classe\n
             2.2- Pour charger la liste des élèves dans une salle vous pouvez :
                2.2.1 - cliquer sur "charger les données depuis un fichier word"; un une fenetre de l'exploreur de \n
                fichier va s'ouvre et vous n'aurez qu'à choisir le fichier contenant la liste des élèves 
                2.2.2 - glisser deposer un fichier dans l'application
                2.2.3 - les données sont modifié et ajouter automatiquement
            3: Avant de lancer le trie vous devez :
            3.1 - Sélectionner les sallles
            3.2 - Sélectionner les classes
            3.3 - Après avoir sélectionner les salles et les classes, appuyer sur trier pour pouvoir trier les élèves dans les salles 
            3.4 - lorsque le trie a été effectué, vous pouvez soit imprimer en pdf, imprimer en word ou voir l'apperçue
            
            * lorsque la l'application plante vous pouvez redémarrer l'application.
                \nCe logiciel a été développé pour le service de la scolarité du CFI-CIRAS
            """
        )
        self.setGeometry(10, 200, 100, 80)

        self.setting_layout.addWidget(self.label, 1, 0, 2, 1)
        self.setting_layout.addWidget(QtWidgets.QLabel(""), 2, 0, 1, 1)
        self.setting_layout.addWidget(QtWidgets.QLabel(""), 3, 0, 1, 1)
        self.setting_layout.addWidget(QtWidgets.QLabel(""), 4, 0, 1, 1)
        self.setting_layout.addWidget(QtWidgets.QLabel(""), 5, 0, 1, 1)

        self.setting_layout.addWidget(QtWidgets.QLabel("Auteur Jim IKOUNGA Teddy Junior"), 6, 0, 1, 1)
        self.setting_layout.addWidget(QtWidgets.QLabel("Contact : +242-06-403-84-79"), 6, 1, 1, 1)
        self.setting_layout.addWidget(QtWidgets.QLabel("version 1.0.0"), 7, 0, 1, 1)

    def setup_connections(self):
        self.btn_parametrage.clicked.connect(lambda x: self.change_widgets("setting"))
        self.btn_gerer_classe.clicked.connect(lambda x: self.change_widgets("classe"))
        self.btn_gerer_salle.clicked.connect(lambda x: self.change_widgets("salle"))
        self.btn_gerer_repartition.clicked.connect(lambda x: self.change_widgets("repartition"))
        # salle
        self.btn_create_salle.clicked.connect(self.create_salle)
        self.sb_limite.valueChanged.connect(self.save_salle)
        self.lw_salle.itemSelectionChanged.connect(self.populate_salle)
        QtGui.QShortcut(QtGui.QKeySequence("Backspace"), self.lw_salle, self.delete_selected_salle)
        self.btn_delete_salle.clicked.connect(self.delete_selected_salle)
        # classe
        self.btn_create_classe.clicked.connect(self.create_classe)
        self.lw_classe.itemSelectionChanged.connect(self.populate_classe)
        self.btn_load_classe_word.clicked.connect(self.get_fichier_word)
        QtGui.QShortcut(QtGui.QKeySequence("Backspace"), self.lw_classe, self.delete_selected_classe)
        self.btn_delete_classe.clicked.connect(self.delete_selected_classe)
        # repartition
        self.lw_repartition_salle.itemClicked.connect(self.toggle_color_salle)
        self.lw_repartition_classe.itemClicked.connect(self.toggle_color_classe)
        self.cb_classe.stateChanged.connect(self.check_all_classe)
        self.cb_salle.stateChanged.connect(self.check_all_salle)
        self.btn_trier.clicked.connect(self.trier)

        self.btn_appercu.clicked.connect(self.appercue)
        self.btn_imprimer_word.clicked.connect(self.print_dialog_word)
        self.btn_imprimer_pdf.clicked.connect(self.print_dialog_pdf)

        # Préferences et paramétrage

    # color change list
    def toggle_color_salle(self, lw_salle_item):
        lw_salle_item.toggle_color()
        self.count_places_total()

    def toggle_color_classe(self, lw_classe_item):
        lw_classe_item.toggle_color()
        self.count_effectif_total()

    def reload_classes_repartition(self):
        self.lw_repartition_classe.clear()
        classes = get_classes()
        for classe in classes:
            if classe.effectif > 0:
                self.add_classe_repartition_listwidget(classe)

    def reload_salles_repartition(self):
        self.lw_repartition_salle.clear()
        salles = get_salles()
        for salle in salles:
            if salle.limite > 0:
                self.add_salle_repartition_listwidget(salle)

    def check_all_classe(self):
        if self.cb_classe.isChecked():
            for i in range(self.lw_repartition_classe.count()):
                item_classe = self.lw_repartition_classe.item(i)
                if not item_classe.select:
                    item_classe.toggle_color()
        else:
            veriter = []
            for i in range(self.lw_repartition_classe.count()):
                item_classe = self.lw_repartition_classe.item(i)
                veriter.append(item_classe.select)

            if False not in veriter:
                for i in range(self.lw_repartition_classe.count()):
                    item_classe = self.lw_repartition_classe.item(i)
                    item_classe.toggle_color()

        self.count_effectif_total()

    def check_all_salle(self):
        if self.cb_salle.isChecked():
            for i in range(self.lw_repartition_salle.count()):
                item_salle = self.lw_repartition_salle.item(i)
                if not item_salle.select:
                    item_salle.toggle_color()
        else:
            veriter = []
            for i in range(self.lw_repartition_salle.count()):
                item_salle = self.lw_repartition_salle.item(i)
                veriter.append(item_salle.select)

            if False not in veriter:
                for i in range(self.lw_repartition_salle.count()):
                    item_salle = self.lw_repartition_salle.item(i)
                    item_salle.toggle_color()

        self.count_places_total()

    def count_places_total(self):
        total, var = 0, 0
        for i in range(self.lw_repartition_salle.count()):
            item_salle = self.lw_repartition_salle.item(i)
            if item_salle.select:
                total += item_salle.salle.limite
                var += 1
        if self.lw_repartition_salle.count() == var:
            self.cb_salle.setCheckState(QtCore.Qt.Checked)
        elif self.lw_repartition_salle.count() != var and var != 0:
            self.cb_salle.setCheckState(QtCore.Qt.Unchecked)
        elif var == 0:
            self.cb_salle.setCheckState(QtCore.Qt.Unchecked)
        self.label_effectif_total_salle.setText(str(total))

    def count_effectif_total(self):
        total, var = 0, 0
        for i in range(self.lw_repartition_classe.count()):
            item_classe = self.lw_repartition_classe.item(i)
            if item_classe.select:
                total += item_classe.classe.effectif
                var += 1
        if self.lw_repartition_classe.count() == var:
            self.cb_classe.setCheckState(QtCore.Qt.Checked)
        elif self.lw_repartition_classe.count() != var and var != 0:
            self.cb_classe.setCheckState(QtCore.Qt.Unchecked)
        elif var == 0:
            self.cb_classe.setCheckState(QtCore.Qt.Unchecked)
        self.label_effectif_total_classe.setText(str(total))

    def show_and_hide_message(self):
        if not self.salles or len(self.salles) == 0:
            self.btn_imprimer_pdf.setEnabled(False)
            self.btn_imprimer_pdf.setToolTip(
                "Bouton désactiver, veuiller d'abord trier les étudiants dans les salles !")
            self.btn_imprimer_word.setEnabled(False)
            self.btn_imprimer_word.setToolTip(
                "Bouton désactiver, veuiller d'abord trier les étudiants dans les salles !")
            self.btn_appercu.setEnabled(False)
            self.btn_appercu.setToolTip("Bouton désactiver, veuiller d'abord trier les étudiants dans les salles !")

        else:
            self.btn_imprimer_pdf.setEnabled(True)
            self.btn_imprimer_pdf.setToolTip("Clicquer pour imprimer en pdf.")
            self.btn_imprimer_word.setEnabled(True)
            self.btn_imprimer_word.setToolTip("Clicquer pour générer le fichier word.")
            self.btn_appercu.setEnabled(True)
            self.btn_appercu.setToolTip("Clicquer pour voir un apperçu.")

    # end
    def add_action_to_toolbar(self):
        widgets = ["home", "salle", "classe", "repartition", "setting"]
        for widget in widgets:
            action = self.toolbar.addAction(widget.capitalize())
            action.triggered.connect(partial(self.change_widgets, widget))

    def change_widgets(self, widget):
        eval(f"self.stack.setCurrentWidget(self.{widget}_widget)")

    def add_salle_to_listwidget(self, salle):
        lw_item = QtWidgets.QListWidgetItem(salle.libelle)
        lw_item.salle = salle
        self.lw_salle.addItem(lw_item)

    def add_classe_to_listwidget(self, classe):
        lw_item = QtWidgets.QListWidgetItem(classe.libelle)
        lw_item.classe = classe
        self.lw_classe.addItem(lw_item)

    def add_classe_repartition_listwidget(self, classe):
        if classe.effectif > 0:
            ClasseItem(classe, list_widget=self.lw_repartition_classe)

    def add_salle_repartition_listwidget(self, salle):
        if salle.limite > 0:
            SalleItem(salle, list_widget=self.lw_repartition_salle)

    def fill_classe_twidget(self, classe: Classe):
        self.tw_classe.setRowCount(len(classe.get_liste()))
        for etudiant in enumerate(classe.get_liste()):
            for ligne in enumerate(["noms", "prenoms", "sexe"]):
                item = QtWidgets.QTableWidgetItem()
                item.setText(etudiant[1].dico().get(ligne[1]))
                self.tw_classe.setItem(etudiant[0], ligne[0], item)
        self.reload_classes_repartition()

    def create_salle(self):
        title, resultat = QtWidgets.QInputDialog.getText(self, "Ajouter une salle", "Nom de la salle : ")
        if resultat and title:
            salle = Salle(libelle=title)
            salle.save()
            self.add_salle_to_listwidget(salle)
            self.add_salle_repartition_listwidget(salle)

    def create_classe(self):
        title, resultat = QtWidgets.QInputDialog.getText(self, "Ajouter une classe", "Nom de la classe : ")
        if resultat and title:
            classe = Classe(name=title)
            classe.save()
            self.add_classe_to_listwidget(classe)
            self.add_classe_repartition_listwidget(classe)

    def get_selected_lw_item(self, lw: QtWidgets.QListWidget):
        selected_items = lw.selectedItems()
        if selected_items:
            self.lb_select.setVisible(False)
            return selected_items[0]
        return None

    def delete_selected_salle(self):
        selected_item = self.get_selected_lw_item(self.lw_salle)
        if selected_item:
            resultat = selected_item.salle.delete()
            if resultat:
                self.lw_salle.takeItem(self.lw_salle.row(selected_item))

        self.reload_salles_repartition()

    def delete_selected_classe(self):
        selected_item = self.get_selected_lw_item(self.lw_classe)
        if selected_item:
            resultat = selected_item.classe.delete()
            if resultat:
                self.lw_classe.takeItem(self.lw_classe.row(selected_item))
        self.reload_classes_repartition()

    def populate_salles(self):
        salles = get_salles()
        for salle in salles:
            self.add_salle_to_listwidget(salle)
            self.add_salle_repartition_listwidget(salle)

    def populate_classes(self):
        classes = get_classes()
        for classe in classes:
            self.add_classe_to_listwidget(classe)
            self.add_classe_repartition_listwidget(classe)

    def calcule_table_banc(self):
        selected_item = self.get_selected_lw_item(self.lw_salle)
        if selected_item:
            self.table_banc.setText(f"{int(self.sb_limite.value()) // 2 + int(self.sb_limite.value()) % 2}")
        else:
            self.table_banc.setText("0")

    def populate_salle(self):
        selected_item = self.get_selected_lw_item(self.lw_salle)
        if selected_item:
            self.sb_limite.setValue(int(selected_item.salle.limite))
            self.le_libelle.setText(selected_item.salle.libelle)
        else:
            self.sb_limite.clear()
            self.le_libelle.clear()

    def populate_classe(self):
        selected_item = self.get_selected_lw_item(self.lw_classe)
        if selected_item:
            self.fill_classe_twidget(selected_item.classe)
        else:
            self.tw_classe.setRowCount(0)

    def save_salle(self):
        selected_item = self.get_selected_lw_item(self.lw_salle)
        if selected_item:
            selected_item.salle.limite = self.sb_limite.value()
            selected_item.salle.save()
            self.calcule_table_banc()
        self.reload_salles_repartition()

    def dragEnterEvent(self, event):
        if self.get_selected_lw_item(self.lw_classe):
            self.lb_drop.setVisible(True)
            event.accept()
        else:
            self.lb_select.setVisible(True)

    def dragLeaveEvent(self, event):
        self.lb_drop.setVisible(False)

    def dropEvent(self, event):
        selected_item = self.get_selected_lw_item(self.lw_classe)
        event.accept()
        self.urls = []
        for url in event.mimeData().urls():
            self.urls.append(url.toLocalFile())
        self.lb_drop.setVisible(False)
        self.startup(self.urls, selected_item.classe)

    def startup(self, path, classe):
        self.thread = QtCore.QThread(self)
        self.worker = Worker(classe, path)
        self.worker.moveToThread(self.thread)
        self.worker.fill.connect(self.fill_classe_twidget)
        self.thread.started.connect(self.worker.write_word_to_json)
        self.worker.finished.connect(self.thread.quit)
        self.thread.start()

    def start_repartition(self, repartition: Repartition):
        self.thread2 = QtCore.QThread(self)
        self.trie_thread = TrieThread(repartition)
        self.trie_thread.moveToThread(self.thread2)
        self.trie_thread.trierend.connect(self.end_triage)
        self.thread2.started.connect(self.trie_thread.triage)
        self.trie_thread.finishe.connect(self.thread2.quit)
        self.thread2.start()

    def get_fichier_word(self):
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setModal(True)
        file_dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        file_dialog.setFilter(QtCore.QDir.Files)

        if file_dialog.exec_():
            file_name = file_dialog.selectedFiles()
            if len(file_name) == 1:
                selected_item = self.get_selected_lw_item(self.lw_classe)
                if selected_item:
                    self.startup(file_name, selected_item.classe)
                    self.reload_classes_repartition()

    def end_triage(self, ok):
        if ok:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information, "Succes",
                                  """Trie effectué avec succcès !\nVous pouvez imprimer ou voir un apperçu.""").exec_()
            self.show_and_hide_message()
        else:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information, "Erreur",
                                  """Trie non effectué !\nVeuillez réessayer.""").exec_()

    def trier(self):
        self.salles.clear()
        if int(self.label_effectif_total_classe.text()) > int(self.label_effectif_total_salle.text()):
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "Protocole de répartition",
                                  """Le nombre d'étudiants est supérieur au nombre de places.\n Veuiller Créer ou 
                                  ajouter une salle !""").exec_()
        elif len(get_selected_repartition_list(self.lw_repartition_classe)) < 2 or len(
                get_selected_repartition_list(self.lw_repartition_salle)) < 2:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "Protocole de selection",
                                  "Sélectionner au moins deux classes et deux salles avant de lancer le trie !").exec_()
        else:
            for item_salle in get_selected_repartition_list(self.lw_repartition_salle):
                self.salles.append(ImpressionSalle(item_salle.salle.libelle, limite=int(item_salle.salle.limite)))
            classes = []
            for item_classe in get_selected_repartition_list(self.lw_repartition_classe):
                classes.append(Classe(name=item_classe.classe.libelle))

            repartition = Repartition()
            for classe in classes:
                classe.load_liste()
                repartition.add_classe(classe)

            for salle in self.salles:
                repartition.add_salle(salle)

            self.start_repartition(repartition=repartition)

    def appercue(self):
        printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
        printer.setPdfVersion(QtGui.QPagedPaintDevice.PdfVersion(2))

        html_pdf = ""
        for salle in self.salles:
            html_pdf += salle.impression_html()

        if html_pdf != "":
            doc = QtGui.QTextDocument()
            doc.setHtml(html_pdf)
            doc.print_(printer)

            previewdialog = QtPrintSupport.QPrintPreviewDialog(printer)
            previewdialog.paintRequested.connect(lambda x: doc.print_(printer))
            previewdialog.exec()

    def print_dialog_pdf(self):
        printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
        printer.setPdfVersion(QtGui.QPagedPaintDevice.PdfVersion(2))

        pdialog = QtPrintSupport.QPrintDialog(printer)
        pdialog.exec()

        html_pdf = ""
        for salle in self.salles:
            html_pdf += salle.impression_html()

        if html_pdf != "":
            self.doc = QtGui.QTextDocument()
            self.doc.setHtml(html_pdf)
            self.doc.print_(printer)

    def print_dialog_word(self):
        word = Word()
        for salle in self.salles:
            word.add_heading(text=salle.nom, taille=0)
            for nom_classe, liste_etudiant in salle.ensemble.items():
                word.add_heading(text=nom_classe, taille=1)
                word.head_table(["N°", "Nom(s)", "prenom(s)", "sexe"])
                word.add_collections(liste_etudiant)
            word.break_new_section()
        word.save()
        word.open()

        q = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information, "Succes",
                                  """Fichier word généreé !\n Veuiller Patienter...""")
        q.exec()
