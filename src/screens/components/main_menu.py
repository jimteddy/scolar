from PySide6 import QtWidgets, QtGui, QtCore


class MainMenuBar(QtWidgets.QWidget):
    def __init__(self, menuBar: QtWidgets.QMenuBar, parent: QtCore.QObject=None):
        super().__init__()
        self.menuBar = menuBar
        self.parent = parent

        self.file = self.menuBar.addMenu("Fichier")
        save = QtGui.QAction("Save", self.parent)
        self.file.addAction("New")
        self.file.addAction(save)
        self.file.triggered[QtGui.QAction].connect(self.processtrigger)

        self.parametre = QtGui.QAction("Paramêtre1", self.parent)
        self.menuBar.addAction(self.parametre)
        self.menuBar.triggered.connect(self.processtriggertest)

    def processtrigger(self, q):
        print(f"{q.text()} is trggered")

    def processtriggertest(self, q):
        print(f"{q.text()} is trggeredtest")

