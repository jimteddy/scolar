from PySide6 import QtWidgets, QtGui

def layout_widget_color(color):
    return QtWidgets.QWidget()

class Stack(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SCOLAR")
        self.setMinimumSize(500, 400)
        self.setGeometry(300, 50, 10, 10)
        self.setStyleSheet(""" background-color: #ccc; color: #000; """)

        self.setup_ui()
        self.setup_data()

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.setup_layouts()
        self.setup_connections()

    def setup_data(self):
        pass

    def create_widgets(self):
        self.leftList = QtWidgets.QListWidget()

        self.leftList.insertItem(0, "Contact")
        self.leftList.insertItem(0, "Personal")
        self.leftList.insertItem(0, "Educationale")
        self.leftList.insertItem(0, "tabs")
        self.leftList.insertItem(1, "test")

        self.stack1 = QtWidgets.QWidget()
        self.stack2 = QtWidgets.QWidget()
        self.stack3 = QtWidgets.QWidget()
        self.stack4 = QtWidgets.QWidget()

        self.stack1UI()
        self.stack2UI()
        self.stack3UI()
        self.stack3UI()

        self.Stacka = QtWidgets.QStackedWidget(self)
        self.Stacka.addWidget(self.stack1)
        self.Stacka.addWidget(self.stack2)
        self.Stacka.addWidget(self.stack3)
        self.Stacka.addWidget(self.stack4)

        hbox = QtWidgets.QHBoxLayout(self)
        hbox.addWidget(self.leftList)
        hbox.addWidget(self.Stacka)

        self.setLayout(hbox)
        self.leftList.currentRowChanged.connect(self.display)
        self.show()

    def modify_widgets(self):pass

    def setup_layouts(self): pass

    def setup_connections(self): pass

    def stack1UI(self):
        layout = QtWidgets.QFormLayout()
        layout.addRow("Name", QtWidgets.QLineEdit())
        layout.addRow("Adresse", QtWidgets.QLineEdit())
        self.stack1.setLayout(layout)

    def stack2UI(self):
        layout = QtWidgets.QFormLayout()
        sex = QtWidgets.QHBoxLayout()
        sex.addWidget(QtWidgets.QRadioButton("Male"))
        sex.addWidget(QtWidgets.QRadioButton("Female"))
        layout.addRow(QtWidgets.QLabel("Name"), sex)
        layout.addRow("Date de naissance", QtWidgets.QLineEdit())
        self.stack2.setLayout(layout)

    def stack3UI(self):
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(QtWidgets.QLabel("subjects"))
        layout.addWidget(QtWidgets.QCheckBox("Maths"))
        layout.addWidget(QtWidgets.QCheckBox("physics"))
        self.stack3.setLayout(layout)

    def stack4UI(self):
        layout = QtWidgets.QHBoxLayout()
        tabs = QtWidgets.QTabWidget()
        tabs.setTabPosition(QtWidgets.QTabWidget.West)
        tabs.setMovable(True)
        for n, color in enumerate(["red", "green", "blue"]):
            tabs.addTab(, color)
        layout.addWidget(tabs)
        self.stack4.setLayout(layout)

    def display(self, index):
        self.Stacka.setCurrentIndex(index)
        print(self.leftList.currentIndex())

