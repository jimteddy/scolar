from PySide6 import QtCore

from docx import Document

from .api.classe import Classe, Etudiant
from .api.repartition import Repartition


class Worker(QtCore.QObject):
    finished = QtCore.Signal()
    fill = QtCore.Signal(Classe)

    def __init__(self, classe, word_path=None):
        super(Worker, self).__init__()
        self.path_word = word_path
        self.classe = classe

    def write_word_to_json(self):

        if self.path_word:
            if isinstance(self.path_word, list):
                self.path_word = self.path_word[0]
                print('-1', self.path_word)

            if self.path_word.endswith('.docx') or self.path_word.endswith('.doc'):
                print("2-")
                doc = Document(self.path_word)
                print(doc)
                liste_et = []
                tables = doc.tables
                try:
                    for table in tables:
                        for row in table.rows[1:]:
                            lis = []
                            for cell in row.cells:
                                lis.append(cell.text)
                            et = Etudiant(lis[1], lis[2], sexe=lis[3], classe=self.classe.libelle)
                            liste_et.append(et.dico())
                    if isinstance(self.classe, str):
                        self.classe = Classe(self.classe)
                    self.classe.set_liste(liste_et)
                    self.classe.save()
                    self.fill.emit(self.classe)
                    self.finished.emit()
                except EnvironmentError:
                    raise "Une erreur système est survenue !"

            else:
                print('pb')


class TrieThread(QtCore.QObject):
    finishe = QtCore.Signal()
    trierend = QtCore.Signal(bool)

    def __init__(self, repartition: Repartition):
        super(TrieThread, self).__init__()
        self.repartition = repartition

    def triage(self):
        print("go trie")
        try:
            self.repartition.placement()
            ok = True
            self.trierend.emit(ok)
            self.finishe.emit()
        except EnvironmentError:
            raise "env erreur"

