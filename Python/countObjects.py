# coding=utf-8
"""
Ville de Lausanne - Routes et mobilité
R Cordonier 01/2019
Traitement et conversions des fichiers des compteurs Golden River et MetroCount en un format de sortie normalisé
Selon le point 7.2 du CDC
Classe objets
"""

# Import des modules nécessaires
from datetime import date, datetime, time, timedelta


class Compteur:
    """ Classe qui définit un comptage
        variables statiques - déclaration
    """
    noCompteur = 0  # numéro selon attribution RM
    e_Date = 2019  # Date de l'échantillon
    e_Heure = 0  # Heure comptage
    canal_1 = 0  # canaux attribués numérique max 4 digits
    canal_2 = 0
    canal_3 = 0
    canal_4 = 0
    canal_5 = 0
    canal_6 = 0

    #fait le lien avec les variables statiques et locales
    def __init__(self, no=0, da=0, h=0, c1=0, c2=0, c3=0, c4=0, c5=0, c6=0):
        self.noCompteur = no
        self.e_Date = da
        self.e_Heure = h
        self.canal_1 = c1
        self.canal_2 = c2
        self.canal_3 = c3
        self.canal_4 = c4
        self.canal_5 = c5
        self.canal_6 = c6

    #
    def __repr__(self):
        return "noCompteur = {0:6d}, e_Date = {1:6d}, e_Heure = {2:4d}, canal_1 = {3:4d}, canal_2 = {4:4d}, canal_3 = {5:4d}, canal_4 = {6:4d}, canal_5 = {7:4d}, canal_6 = {8:4d}".format(
            self.noCompteur,
            self.e_Date,
            self.e_Heure,
            self.canal_1,
            self.canal_2,
            self.canal_3,
            self.canal_4,
            self.canal_5,
            self.canal_6
        )

    def valeurs(self):
            return "{0:06d} {1:06d} {2:04d} {3:04d} {4:04d} {5:04d} {6:04d} {7:04d} {8:04d}".format(
                self.noCompteur,
                self.e_Date,
                self.e_Heure,
                self.canal_1,
                self.canal_2,
                self.canal_3,
                self.canal_4,
                self.canal_5,
                self.canal_6
            )



"""class compteur_1_mois:
    #compteur1mois = cpt.Compteur.valeurs()
    M720data =rdM720.CounterM720.readFile('Z:\Python\PY_Code\C036TUN_I6X.txt')
    print(rdM720.CounterM720.M720affectCanal)
    #une ligne représente 12h
    nbreLigne1Jour = rdM720.CounterM720.M720affectCanal * 2 #pour 24h
    noCompteur = rdM720.CounterM720.M720Compteur"""


if __name__ == '__main__':
    import sys

    #compteur_1_mois.append(Compteur(103, 10219, 200, 10, 20, 30, 40, 50, 60))
    #compteur_1_mois.append(Compteur(103, 10219, 1400, 100, 200, 300, 400, 500, 600))

    print('test')
    test = Compteur()

    print(test.__repr__())

    print('fin de test')
