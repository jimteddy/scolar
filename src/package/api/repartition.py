import random

from .classe import Etudiant
from .salle import choix


class Repartition:

    def __init__(self):
        self.place = []
        self.salles = []
        self.classes = []
        self.liste_total = []

    @property
    def total_etudiant(self):
        eff = 0
        for element in self.classes:
            eff += element.effectif
        return eff

    @property
    def total_place(self):
        total_dispo = 0
        for element in self.salles:
            total_dispo += element.nombre
        return total_dispo

    def add_salle(self, salle: 'Salle'):
        self.salles.append(salle)

    def add_classe(self, classe: 'Classe'):
        self.classes.append(classe)

    def _trie_salle(self, croissant=True):
        if croissant:
            for i in range(len(self.salles) - 1, 0, -1):
                for j in range(i):
                    if self.salles[j].nombre < self.salles[j + 1].nombre:
                        temp = self.salles[j]
                        self.salles[j] = self.salles[j + 1]
                        self.salles[j + 1] = temp
        else:
            for i in range(len(self.salles) - 1, 0, -1):
                for j in range(i):
                    if self.salles[j].nombre > self.salles[j + 1].nombre:
                        temp = self.salles[j]
                        self.salles[j] = self.salles[j + 1]
                        self.salles[j + 1] = temp

    def _trie_classes(self, croissant=True):
        if croissant:
            for i in range(len(self.classes) - 1, 0, -1):
                for j in range(i):
                    if self.classes[j].effectif < self.classes[j + 1].effectif:
                        temp = self.classes[j]
                        self.classes[j] = self.classes[j + 1]
                        self.classes[j + 1] = temp
        else:
            for i in range(len(self.classes) - 1, 0, -1):
                for j in range(i):
                    if self.classes[j].effectif > self.classes[j + 1].effectif:
                        temp = self.classes[j]
                        self.classes[j] = self.classes[j + 1]
                        self.classes[j + 1] = temp

    def salle_dispo(self):
        liste = set()
        for salle in self.salles:
            print("dispo", salle.disponible)
            if salle.disponible != 0:
                liste.add(salle)

        if len(liste) != 0:
            for lis in liste:
                print(lis.nom, lis.disponible)
        else:
            print('plus de salle libre')

    def placement(self):
        if self.total_place < self.total_etudiant:
            print("effectif total d'etudiant :", self.total_etudiant)
            print("Nombre total de place :", self.total_place)
            return False, "Ajouter une salle, nombre d'étudiant > au nombre de place dans les salles"
        else:
            for salle in self.salles:
                salle.init_bancs()

            for classe in self.classes:
                for etudiant in classe.get_liste():
                    self.liste_total.append(etudiant)

            while len(self.liste_total) != 0:
                for salle in self.salles:
                    element = choix(self.liste_total)
                    long = random.randint(0, len(salle.bancs) - 1)
                    if salle.bancs[long].attribution(element):
                        self.place.append(element)
                    else:
                        self.liste_total.append(element)

                    if len(self.liste_total) == 0:
                        break

            for salle in self.salles:
                for banc in salle.bancs:
                    for rang in banc.get():
                        if rang is not None:
                            salle.add_element(rang)

            for salle in self.salles:
                salle.trie_avant_impression()
                salle.sort_by_banc_in_ensemble()
                #salle.sort_by_name_in_ensemble()
