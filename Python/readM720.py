"""
Ville de Lausanne - Routes et mobilité
R Cordonier 01/2019
Traitement et conversions des fichiers des compteurs Golden River et MetroCount en un format de sortie normalisé
Selon le point 7.2 du CDC
lecture du fichier donné
"""
# Import des modules nécessaires
import os, linecache
import numpy as np
import setup
from datetime import datetime


class ReadM720:

    # fait le lien avec les variables statiques et locales - constructeur
    def __init__(self, nocompt=0, nbrecan=0, affectcanal=0, ddebut=0, hdebut=0, dfin=0, hfin=0):
        self.compteur_nom = 'a'  #
        self.nbre_canal = nbrecan
        self.affect_canal = []
        self.date_debut = ddebut
        self.heure_debut = hdebut
        self.date_fin = dfin
        self.heure_fin = hfin
        self.data_ascii = []
        self.InitTableau()

    def __repr__(self):
        return 'no de Compteur {0: 6d}, Nbre de canaux = {1:6d}, affectation des canaux = {2:6d}, date de début = {3:6d}, heure de début = {4:4d}, date de fin = {5:6d}, heure de fin = {6:4d}'.format(
            self.compteur_nom,
            self.nbre_canal,
            self.affect_canal,
            self.date_debut,
            self.heure_debut,
            self.date_fin,
            self.heure_fin)

    def readFile(self, fName=r'.\Data\C105CHAB_I6E.txt'):
        fName.replace('\\', '/')
        # ouverture du fichier en lecture, instanciation de la variable "iteration" qui nous servira d'index
        with open(fName, 'r') as file:
            iteration = 0
            # pour chaque ligne(ici représentée par lines) dans le fichier
            for lines in file.readlines():
                # si le premier mot de la ligne est un chiffre, alors split de la ligne en mots puis insertion de chaque mot dans le tab data
                if lines[0].isdigit():
                    words = lines.split()
                    self.data_ascii.append(words)
                    # du moment que la var iteration est inférieure ou égale à la longeure du tab data alors prendre 1e mot de la ligne et l'injecter dans la var iterationDate
                    iterationDate = self.data_ascii[iteration][0]
                    # conversion de 2 carcatères (sélectionnés par des []) de la var string iterationDate en int puis multiplication de ceux-ci selon la position souhaitée pour obtenir le format de sortie désiré
                    iterDateFormatSortie = (iterationDate[-2:]) + (iterationDate[-4:-2]) + (iterationDate[:2])
                    print(iterDateFormatSortie)
                    # Insertion de la var iterDateFormatSortie dan sla première positin de chaque ligne du tab data
                    self.data_ascii[iteration][0] = iterDateFormatSortie
                    # incrémentation de la var iteration
                    iteration += 1
                    self.PrintData(r'test_in.txt', self.data_ascii)

                    # si le mot "SITE" se trouve dans une des lignes, alors split la phrase
                if "SITE" in lines:
                    words = lines.split()
                    # pour chaque lettre dans chaque mot de la ligne, s'il est composé de chiffres alors le mot est affecté à la variable M720Compteur
                    for b in words:
                        if b.isdigit():
                            # self.compteur_nom.__add__(b)
                            self.compteur_nom = b

                # si le mot "CHANNELS" se trouve dans une des lignes, alors split la phrase
                if "CHANNELS" in lines:
                    words = lines.split()
                    # pour chaque lettre dans chaque mot de la ligne, s'il est composé de chiffres alors le mot est intégré dans le tab M720affectCanal
                    for b in words:
                        if b.isdigit():
                            self.affect_canal.append(int(b))
                            self.nbre_canal = len(self.affect_canal)
                # si le mot "STARTREC" se trouve dans une des lignes, alors split la phrase, prend le dernier mot du tableau words et remplace les "/" par rien puis affecte le mot à la var M720dateDebut
                if "STARTREC" in lines:
                    words = lines.split()
                    strDateDebut = words[-1].replace('/', '')
                    self.date_debut = strDateDebut

    def PrintData(self, file, tableau_a_imprimer):
        with open(file, 'w') as file:
            for ligne in tableau_a_imprimer:
                file.write(str(ligne))
                file.write('\n')

    def InitTableau(self):
        jour_date = 1
        i = 0
        heures = 100
        self.data_int = np.zeros((744, 9), dtype=int)
        while i < (31 * 24):
            self.data_int[i][1] = jour_date
            self.data_int[i][2] = heures
            heures += 100
            if heures > 2400:
                jour_date = jour_date + 1
                heures = 100
            i += 1
        print(self.data_int)
        self.PrintData(r'test_out.txt', self.data_int)

    def lecturePremierJour(self, fName=r'.\Data\C105CHAB_I6E.txt'):
        fName.replace('\\', '/')
        with open(fName, 'r') as file:
            # pour chaque ligne(ici représentée par lines) dans le fichier
            for lines in file.readlines():
                # si le premier mot de la ligne est un chiffre, alors split de la ligne en mots puis insertion du 1er mot dans la var locale date
                if lines[0].isdigit():
                    words = lines.split()
                    date = words[0]
                    jour = date[0:2]
                    print(jour)
                    while jour >= "01":
                        self.readFile()

    def CanRead(self, can_source):
        return setup.par['can'][can_source]


if __name__ == '__main__':
    import sys

    x = ReadM720()
    x.readFile(r'.\Data\C105CHAB_I6E.txt')

    print("---------------\n")

    # print(x.compteur_nom)
    # print(x.affect_canal)
    # print(x.nbre_canal)
    # print(x.date_debut)
    # print(x.CanRead(2))
    print(x.lecturePremierJour)
