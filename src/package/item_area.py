from PySide6 import QtCore, QtGui, QtWidgets

COLORS = {False: (42, 127, 255), True: (12, 53, 97)}


class SalleItem(QtWidgets.QListWidgetItem):
    def __init__(self, salle: 'Salle', list_widget=None):
        super(SalleItem, self).__init__(salle.libelle)
        self.salle = salle
        self.select = False
        self.list_widget = list_widget

        if self.list_widget is not None:
            self.list_widget.addItem(self)
        self.setSizeHint(QtCore.QSize(self.sizeHint().width(), self.sizeHint().height()))
        #self.set_background_color()

    def __str__(self):
        return f"""{self.salle.libelle} ({self.salle.limite})"""

    def __repr__(self):
        return f"""{self.salle.libelle}"""

    def sizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(50, 30)

    def toggle_color(self):
        self.select = not self.select
        self.set_background_color()

    def set_background_color(self):
        color = COLORS.get(self.select)
        self.setBackground(QtGui.QColor(*color))
        color_str = ",".join(map(str, color))
        stylesheet = f""" QListView::item:selected{{ background: rgb({color_str}); color : rgb(255, 255, 255); }}"""
        if self.list_widget is not None:
            self.list_widget.setStyleSheet(stylesheet)


class ClasseItem(QtWidgets.QListWidgetItem):
    def __init__(self, classe: 'Classe', list_widget=None):
        super(ClasseItem, self).__init__(classe.libelle)
        self.select = False
        self.classe = classe
        self.list_widget = list_widget

        self.setSizeHint(QtCore.QSize(self.sizeHint().width(), self.sizeHint().height()))

        if self.list_widget is not None:
            self.list_widget.addItem(self)

    def __str__(self):
        return f"""{self.classe.libelle}"""

    def __repr__(self):
        return f"""{self.classe.libelle}({self.classe.effectif})"""

    def sizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(50, 30)

    def toggle_color(self):
        self.select = not self.select
        self.set_background_color()

    def set_background_color(self):
        color = COLORS.get(self.select)
        self.setBackground(QtGui.QColor(*color))
        color_str = ",".join(map(str, color))
        stylesheet = f""" QListView::item:selected {{ background: rgb({color_str}); color : rgb(255, 255, 255); }}"""
        self.list_widget.setStyleSheet(stylesheet)


if __name__ == '__main__':
    c = ClasseItem("jim", 20)
    print(c)
