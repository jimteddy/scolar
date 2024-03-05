import os
import json
import random
from glob import glob
from uuid import uuid4

from constantes import MATIERE_DIR


def get_matieres():
    matieres = []
    fichiers = glob(os.path.join(MATIERE_DIR, "*.json"))
    for fichier in fichiers:
        with open(fichier, "r") as f:
            matiere_data = json.load(f)
            matiere_uuid = os.path.splitext(os.path.basename(fichier))[0]
            matiere_libelle = matiere_data.get("libelle")
            matiere_coefficient = matiere_data.get("coefficient")
            m = Matiere(libelle=matiere_libelle, coefficient=matiere_coefficient, uuid=matiere_uuid)
            matieres.append(m)
    return matieres


class Matiere:
    def __init__(self, libelle, coefficient, uuid=None):
        if uuid:
            self.uuid = uuid
        else:
            self.uuid = str(uuid4())
        self.libelle = libelle
        self.coefficient = coefficient

    def __repr__(self):
        return f"{self.libelle} ({self.uuid})"

    def __str__(self):
        return self.libelle

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
