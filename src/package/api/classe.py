import os
import json
from glob import glob
import random

from .constantes import Classe_Dir


def get_etudiant_from_dictionnaire(dictionnaire: {}, classe: str):
    return Etudiant(dictionnaire.get('noms'), dictionnaire.get('prenoms'), sexe=dictionnaire.get('sexe'), classe=classe)


def get_classes():
    classes = []
    fichiers = glob(os.path.join(Classe_Dir, "*.json"))
    for fichier in fichiers:
        with open(fichier, "r") as f:
            try:
                classe_data = json.load(f)
                classe_name = os.path.splitext(os.path.basename(fichier))[0]
                classe = Classe(classe_name)
                for ligne in classe_data:
                    classe.liste.append(ligne)
                classes.append(classe)
            except json.decoder.JSONDecodeError:
                pass
    return classes


class Etudiant:
    def __init__(self, nom, prenom, sexe="", classe=None):
        self.nom = nom
        self.prenom = prenom
        self.sexe = sexe
        self.classe = classe
        self.banc = None

    def __str__(self):
        return f"{self.nom} {self.prenom} {self.sexe} {self.classe} {self.banc}"

    def __repr__(self):
        return f"{self.nom} {self.prenom} {self.sexe} {self.classe} {self.banc}"

    def get(self):
        return self.nom, self.prenom, self.sexe, self.classe, self.banc

    def in_liste(self):
        l = []
        l.append(self.nom)
        l.append(self.prenom)
        l.append(self.sexe)
        l.append(self.banc)
        return l

    def dico(self):
        return {
            'noms': self.nom,
            'prenoms': self.prenom,
            'sexe': self.sexe,
            'banc': self.banc,
            'classe': self.classe
        }


class Classe:
    def __init__(self, name=""):
        self.libelle = name
        self.etudiants = []
        self.liste: list[dict] = []

    @property
    def effectif(self):
        return len(self.liste)

    @property
    def nombre(self):
        return len(self.etudiants)

    def __repr__(self):
        return f"{self.libelle} ({self.effectif}) ({self.nombre})"

    def __str__(self):
        return f"{self.libelle} ({self.effectif}) ({self.nombre})"

    def load_liste(self):
        with open(self.path, "r") as f:
            self.liste = json.load(f)
        self.load_etudiants()

    def load_etudiants(self):
        self.etudiants.clear()
        for dictio in self.liste:
            self.etudiants.append(get_etudiant_from_dictionnaire(dictio, self.libelle))

    def set_liste(self, liste):
        self.liste.clear()
        self.liste = liste
        self.load_etudiants()

    def get_liste(self):
        self.load_liste()
        if len(self.etudiants) == 0:
            return []
        return self.etudiants

    def delete(self):
        os.remove(self.path)
        if os.path.exists(self.path):
            return False
        return True

    def save(self):
        if not os.path.exists(Classe_Dir):
            os.makedirs(Classe_Dir)
        with open(self.path, "w") as f:
            json.dump(self.liste, f, indent=4, ensure_ascii=True)

        print(self.path)

    @property
    def path(self):
        return os.path.join(Classe_Dir, self.libelle + ".json")

    def get_etudiant(self):
        if len(self.etudiants) != 0:
            etudiant = random.choice(self.etudiants)
            if etudiant in self.etudiants:
                self.etudiants.remove(etudiant)
            return etudiant
        else:
            return False


if __name__ == '__main__':
    Classe("Gl").save()
    classes = get_classes()
    print(classes)
