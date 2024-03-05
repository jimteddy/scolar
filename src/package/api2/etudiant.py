
class Etudiant:
    def __init__(self, nom, prenom, classe):
        self.nom = nom
        self.prenom = prenom
        self.classe = classe

    def __str__(self):
        return self.nom

    def __repr__(self):
        return self.nom

    @staticmethod
    def create_liste():
        liste = []
        liste.append(Etudiant("jimik", "ted", "Lic 1"))
        liste.append(Etudiant("lana", "piatri", "Lic 2"))
        liste.append(Etudiant("pakagg", "orly", "Lic 2"))
        liste.append(Etudiant("geremi", "teddy", "Lic 1"))
        return liste