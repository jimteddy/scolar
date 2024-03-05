import os
import json
import random
from glob import glob
from uuid import uuid4

from .classe import Etudiant
from .constantes import Salle_Dir


def alter_nom(nom):
    if nom[:5].upper() == "SALLE":
        name = "SALLE " + nom[6:]
        return name
    return "SALLE " + nom


def get_salles():
    salles = []
    fichiers = glob(os.path.join(Salle_Dir, "*.json"))
    for fichier in fichiers:
        with open(fichier, "r") as f:
            salle_data = json.load(f)
            salle_uuid = os.path.splitext(os.path.basename(fichier))[0]
            salle_libelle = salle_data.get("libelle")
            salle_limite = salle_data.get("limite")
            n = Salle(libelle=salle_libelle, limite=salle_limite, uuid=salle_uuid)
            salles.append(n)
    return salles


def choix(seqs):
    element = random.choice(seqs)
    if element in seqs:
        seqs.remove(element)
    return element


class Salle:
    def __init__(self, libelle="", limite: int = 0, uuid=None):
        if uuid:
            self.uuid = uuid
        else:
            self.uuid = str(uuid4())
        self.libelle = alter_nom(libelle)
        self.limite = limite
        self.banc = 0

    def __repr__(self):
        return f"{self.libelle} ({self.uuid})"

    def __str__(self):
        return self.libelle

    @property
    def limite(self):
        return self._limite

    @limite.setter
    def limite(self, value):
        if isinstance(value, int):
            self._limite = value
        else:
            raise TypeError("Need the nomber")

    def delete(self):
        os.remove(self.path)
        if os.path.exists(self.path):
            return False
        return True

    def save(self):
        if not os.path.exists(Salle_Dir):
            os.makedirs(Salle_Dir)

        data = {"libelle": self.libelle, "limite": self.limite}
        with open(self.path, "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=True)

    @property
    def path(self):
        return os.path.join(Salle_Dir, self.uuid + ".json")


################################################################################

class Table:
    def __init__(self):
        self.etudiant = None
        self.occupation = False


class Place:
    def __init__(self, numero: int, place: "str"):
        self.numero = numero + 1
        self.place = place.capitalize()

    def __str__(self):
        return f"Banc {self.numero} à {self.place}"

    def __repr__(self):
        return f"Banc {self.numero} à {self.place}"


class Banc:
    def __init__(self, num: int):
        self.numero = num
        self.gauche: Table = Table()
        self.droit: Table = Table()

    def __str__(self):
        return f"banc {self.numero}, G({self.gauche.etudiant}, {self.droit.etudiant}) : {self.occupe}"

    def __repr__(self):
        return f"banc {self.numero}, G({self.gauche.etudiant}, {self.droit.etudiant}) : {self.occupe}"

    def attribution(self, element: Etudiant):
        # print(element)
        if not self.occupe:
            if not self.gauche.occupation:
                element.banc = Place(self.numero, "Gauche")
                self.gauche.etudiant = element
                self.gauche.occupation = True
                return True
            elif not self.droit.occupation and self.gauche.etudiant.classe != element.classe:
                element.banc = Place(self.numero, "Droite")
                self.droit.etudiant = element
                self.droit.occupation = True
                return True

            return False
        return False

    def get(self):
        return self.gauche.etudiant, self.droit.etudiant

    @property
    def occupe(self):
        if self.gauche.occupation is True and self.droit.occupation is True:
            return True
        else:
            return False


################################################################################


class ImpressionSalle:
    def __init__(self, nom: str, limite: int = 0):
        self.nom = alter_nom(nom)
        self._element = set()  # tous les element
        self._ensemble = {}  # element classé par classe
        self.nombre = limite
        self.bancs = []
        self.place = {}

    def __str__(self):
        return f"""Nom {self.nom}, place : {self.nombre}, place dispo : {self.disponible}"""

    def __repr__(self):
        return f"""Nom {self.nom}, place : {self.nombre}, place dispo : {self.disponible}"""

    @property
    def disponible(self):
        return self.nombre - self.taille

    @property
    def taille(self):
        tailles = 0
        for k, v in self._ensemble.items():
            for x in v:
                tailles += 1
        return tailles

    @property
    def taille2(self):
        tailles = 0
        for k, v in self.place.items():
            for x in v:
                tailles += 1
        return tailles

    def limite(self, limite):
        self.nombre = limite
        self.init_bancs()

    @property
    def element(self):
        return self._element


    @property
    def ensemble(self):
        return self._ensemble

    def add_element(self, elm: Etudiant):
        if len(self._element) < self.nombre:
            if elm in self._element:
                return False
            else:
                self._element.add(elm)
                return True

    def placement(self):
        for nom_classe, liste_etudiants in self.ensemble.items():
            self.place[nom_classe] = []
            self.nom_place = []
            print(len(self.bancs))
            while len(liste_etudiants) != 0:
                print(len(liste_etudiants))
                element = choix(liste_etudiants)
                long = random.randint(0, len(self.bancs) - 1)
                if self.bancs[long].attribution(element):
                    self.place[nom_classe].append(element)
                else:
                    liste_etudiants.append(element)
                    self.nom_place.append(element)

                if self.bancs[long].occupe:
                    self.bancs.remove(self.bancs[long])
                    continue

    def init_bancs(self):
        nombre_banc = self.nombre // 2 + self.nombre % 2
        for x in range(nombre_banc):
            self.bancs.append(Banc(x))

    def show_banc(self):
        for banc in self.bancs:
            print(banc)

    def choices(self, seqs, nombre_elm_choix=0):
        if nombre_elm_choix == 0:
            self.add_element(choix(seqs))
        else:
            nbr = nombre_elm_choix
            while nbr != 0:
                if self.add_element(choix(seqs)):
                    nbr -= 1
                    if len(self._element) == self.nombre:
                        break

    def trie_avant_impression(self):
        for element in self.element:
            # print(element)
            if element.classe not in self._ensemble.keys():
                self._ensemble[element.classe] = list()
                self._ensemble.get(element.classe).append(element)
            elif element.classe in self._ensemble.keys():
                self._ensemble.get(element.classe).append(element)

    def sort_by_name_in_ensemble(self):
        for nom_classe, liste_etudiant in self.ensemble.items():
            for i in range(len(liste_etudiant) - 1, 0, -1):
                for j in range(i):
                    if liste_etudiant[j].nom > liste_etudiant[j + 1].nom:
                        temp = liste_etudiant[j]
                        liste_etudiant[j] = liste_etudiant[j + 1]
                        liste_etudiant[j + 1] = temp

    def sort_by_banc_in_ensemble(self):
        for nom_classe, liste_etudiant in self.ensemble.items():
            for i in range(len(liste_etudiant) - 1, 0, -1):
                for j in range(i):
                    if liste_etudiant[j].banc.numero > liste_etudiant[j + 1].banc.numero:
                        temp = liste_etudiant[j]
                        liste_etudiant[j] = liste_etudiant[j + 1]
                        liste_etudiant[j + 1] = temp

    def impression_html(self):
        header = f"""<html lang="fr">
                       <head>
                           <meta charset="UTF-8">
                           <meta content="text/html; charset=ISO-8859-1" http-equiv="content-type">
                           <style>
                             h3, legend, h2 {{
                                 text-align: center;
                             }}
                             h2 {{
                               text-decoration: underline;
                               font-size: 15;
                               font-family: "Courir New";
                               font-weight: bold;
                               text-transform: uppercase;
                             }}
                             .nom {{
                                text-transform: uppercase;
                                font-weight: bold;
                                font-size: 16;
                             }}
                             .prenom {{
                                text-transform: capitalize;
                                font-weight: 400;
                                font-size: 13;
                             }}
                             .tde {{
                               font-size: 15;
                               font-weight: bold;
                               text-transform: uppercase;           
                            }}
                           </style>
                       </head>
                       <body style="font-family:sans-serif; page-break-before:always;">
                       <h2>{self.nom}</h2>
                       """

        def body(titre):
            return f"""<br><h2>{titre}</h2>
                        <table border="1" cellpadding="10" cellspacing="0" width="100%"> 
                    """

        footer = """</body></html>"""
        fin_tab = """</tbody></table>                     
                """
        the_html = ""
        thead = """<thead><tr>
                       <td class="tde">N°</td>
                       <td class="tde">Nom(s)</td>
                       <td class="tde">Prenom(s)</td>
                       <td class="tde">Sexe</td>
                     </tr></thead><tbody>
                     """

        def ligne(numero, noms, prenoms, sexe):
            sexe = "" if sexe is None else sexe
            return f"""<tr>
                           <td>{numero}</td>
                           <td><span class="nom" >{noms} </span></td>
                           <td><span class="prenom"> {prenoms}</span></td>
                           <td>{sexe}</td>
                       </tr>
                    """

        the_html += header
        for classe, etudiants in self.ensemble.items():
            the_html += body(classe)
            the_html += thead
            i = 0
            for etudiant in etudiants:
                i += 1
                the_html += ligne(i, f"""{etudiant.nom}""", f""" {etudiant.prenom}""", etudiant.sexe)
            the_html += fin_tab
        the_html += footer

        return the_html


if __name__ == '__main__':
    tes = ImpressionSalle("test", limite=4)
    # salles = get_salles()
    # print(salles)
