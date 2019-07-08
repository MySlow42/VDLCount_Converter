"""
Ville de Lausanne - Routes et mobilité
R Cordonier 01/2019
Traitement et conversions des fichiers des compteurs Golden River et MetroCount en un format de sortie normalisé
Selon le point 7.2 du CDC
recherche tous les fichiers à lire puis traîtement des fichiers
"""
# Import des modules nécessaires
import logging

import time

import numpy as np

import setup


class CounterM720:
    #  variables globales
    liste_nom = []
    jour = ''

    #  paramètre pour le logger
    logging.basicConfig(filename='test_log.log', level=logging.DEBUG,
                        format='%(asctime)s -- %(levelname)s -- %(message)s')
    logging = logging.getLogger('spam')
    t0 = time.time()
    logging.info('Démarrage de {0} -- version {1}'.format(setup.NAME, setup.VERSION))

    """ constructeur qui fait le lien avec les variables statiques et locales
     Prend en paramètre les variables utiles à la classe"""

    def __init__(self, nocompt=0, nbrecan=0, affectcanal=0, ddebut=0, hdebut=0, dfin=0, hfin=0):
        self.compteur_num = 'a'
        self.nbre_canal = nbrecan
        self.affect_canal = []
        self.date_debut = ddebut
        self.heure_debut = hdebut
        self.date_fin = dfin
        self.heure_fin = hfin
        self.data_ascii = []
        # self.initTableau()

    """def __repr__(self):
        return 'no de Compteur {0: 6d}, Nbre de canaux = {1:6d}, affectation des canaux = {2:6d}, date de début = {3:6d}, heure de début = {4:4d}, date de fin = {5:6d}, heure de fin = {6:4d}'.format(
            self.compteur_num,
            self.nbre_canal,
            self.affect_canal,
            self.date_debut,
            self.heure_debut,
            self.date_fin,
            self.heure_fin)"""

    # fonction qui va lire le fichier,contenant le 1er jour, inséré par l'user et déterminer les 4 autres fichiers à lire
    # le r avant le pathfile va empêcher le backslash d'être interprété comme caractère d'échappement en le doublant
    def nomFichierALire(self, nom_premier_fichier='.\Data\C105CHAB_I6s.txt'):
        logging.info('Nom du fichier inséré: {0}'.format(nom_premier_fichier))
        nom_premier_fichier = nom_premier_fichier.replace('\\', '/')  # remplace les \\ en /
        nom_premier_fichier = nom_premier_fichier.upper()  # mise en maj de la chaîne
        path_nom_fichier = nom_premier_fichier[:-6]  # tronquage du pathfile pour obtenir que le nom du fichier
        u = nom_premier_fichier[-5:-4]  # récupération du 1er caractère qui devra être incrémenter
        d = nom_premier_fichier[-6:-5]  # récupération du 2nd caractère qui devra être incrémenter
        extension = nom_premier_fichier[-4:]  # récupération de l'extension
        print(self.liste_nom)
        self.liste_nom.append(nom_premier_fichier)  # insertion du 1er pathfile (donné par l'user)
        nb_fich = 0

        # tant que le nbre de fichier est en dessous de 5
        while nb_fich < 5:
            u = CounterM720.incr09az(self, u)  # appel de la fonction incr09az avec u en paramètre
            if u == '0':  # si u est egal à 0
                d = CounterM720.incr09az(self, d)  # appel de la fonction incr09az avec d en paramètre

            nom = path_nom_fichier + str(d) + str(u) + extension  # contruction du nouveau nom de fichier avec extension
            print(d, u)
            self.liste_nom.append(nom)  # insertion du nouveau nom de fichier dans la liste
            nb_fich += 1  # incrémentation de la var
            print(self.liste_nom)

            # return self.liste_nom

    # fonction qui prend en paramètre qui additione 1 à la variable préalablement convertie en ASCII
    def incr09az(self, charFile):
        if charFile.isdecimal():  # si le caractère est un décimal
            if charFile == '9':  # s'il est égal à 9 retourner A
                return 'A'
            else:
                return chr(ord(
                    charFile) + 1)  # sinon convertir la valeur en Ascii l'additionner à 1 et la reconvertir en décimal
        if charFile.isalpha():  # si la variable est une lettre
            if charFile == 'Z':  # si elle est égale à Z
                return '0'  # retourne 0
            else:
                return chr(ord(charFile) + 1)  # sinon retourne la valeur en Ascii +1
        print('Nom de fichier erroné: ' + self.liste_nom[0])  # sinon renvoyer une erreur à l'user
        exit(1)

    # fonction qui va lire et récupérer les infos utiles dans l'en-tête du fichier SI c'est le fichier qui contient le
    # premier jour, met les valeurs dans le tableau data_ascii avec les dates format aammjj, appel fonction initTableau
    def readFile(self):
        logging.info('Fichiers à traiter: {0}'.format(self.liste_nom))
        nb_fichiers_lus = 0
        nb_fichiers_recus = 0
        index_liste_nom = 0
        iteration_data_ascii: int = 0
        jour_1 = False
        print(self.liste_nom[index_liste_nom])
        for fName in self.liste_nom:
            fName = fName.replace('\\', '/')
            # ouverture du fichier en lecture, instanciation de la variable "iteration_data_ascii" qui nous servira
            # d'index
            with open(fName, 'r') as file:

                # pour chaque ligne(ici représentée par lines) dans le fichier
                for lines in file.readlines():

                    if nb_fichiers_lus == 0:
                        # si le mot "SITE" se trouve dans une des lignes, alors split la phrase
                        if "SITE" in lines:
                            words = lines.split()
                            # pour chaque lettre dans chaque mot de la ligne, s'il est composé de chiffres alors le mot
                            # est affecté à la variable M720Compteur
                            for b in words:
                                if b.isdigit():
                                    # self.compteur_num.__add__(b)
                                    self.compteur_num = b
                                    print('nom compteur ' + str(self.compteur_num))

                        # si le mot "CHANNELS" se trouve dans une des lignes, alors split la phrase
                        if "CHANNELS" in lines:
                            words = lines.split()
                            # pour chaque lettre dans chaque mot de la ligne, s'il est composé de chiffres alors le mot
                            # est intégré dans le tab M720affectCanal
                            for b in words:
                                if b.isdigit():
                                    self.affect_canal.append(int(b))
                                    self.nbre_canal = len(self.affect_canal)
                            print('nbre de canaux ' + str(self.nbre_canal))

                        # # si le mot "STARTREC" se trouve dans une des lignes, alors split la phrase, prend le dernier
                        # mot du tableau words et remplace les "/" par rien puis affecte le mot à la var M720dateDebut
                        # if "STARTREC" in lines:
                        #     words = lines.split()
                        #     strDateDebut = words[-1].replace('/', '')
                        #     self.date_debut = strDateDebut
                        #     print('date de début ' + str(self.date_debut))

                        # si le nbre de fichiers lus est suppérieur ou égal à 0
                    if nb_fichiers_lus >= 0:
                        # si le premier élément dans le tableau est un chiffre alors récupération des 2 derniers
                        # chiffres et les attribuer à la variable jour
                        if lines[0].isdigit():
                            words = lines.split()
                            date = words[0]
                            self.jour = date[0:2]

                            if jour_1 == False:  # premier jour du mois pas encore trouvé
                                # si le premier mot de la ligne est un chiffre, alors split de la ligne en mots puis
                                # insertion de chaque mot dans le tab data

                                if self.jour == "01":
                                    jour_1 = True
                                self.date_debut = date

                            if self.jour == "01" and jour_1 and nb_fichiers_lus > 0:
                                break

                            if jour_1:
                                # print(jour)
                                self.data_ascii.append(words)
                                # du moment que la var iteration_data_ascii est inférieure ou égale à la longeure du tab
                                # data alors prendre 1e mot de la ligne et l'injecter dans la var iterationDate
                                iterationDate = self.data_ascii[iteration_data_ascii][0]
                                # conversion de 2 carcatères (sélectionnés par des []) de la var string iterationDate
                                # en int puis multiplication de ceux-ci selon la position souhaitée pour obtenir le
                                # format de sortie désiré
                                iterDateFormatSortie = (iterationDate[-2:]) + (iterationDate[-4:-2]) + (
                                    iterationDate[:2])
                                # print(self.data_ascii[iteration_data_ascii][0])
                                # Insertion de la var iterDateFormatSortie dans la première position de chaque ligne du
                                # tab data
                                self.data_ascii[iteration_data_ascii][0] = iterDateFormatSortie
                                # incrémentation de la var iteration_data_ascii
                                print(self.data_ascii[iteration_data_ascii][0])
                                iteration_data_ascii += 1

            # imprime les données avec la date dans le bon format dans le fichier de sortie test_in.txt
            self.printData(r'test_in.txt', self.data_ascii)
            # impressime fin du traitement + nom du fichier traiter
            print('Fin du traitement du fichier' + self.liste_nom[index_liste_nom])
            # Incrémente les valeurs de 1
            index_liste_nom += 1
            nb_fichiers_recus += 1  # mettre avant
            nb_fichiers_lus += 1
        # Appel de la fonction suivante
        self.initTableau()

    # fonctione qui imprime les données d'un tableaux dans un fichier externe
    def printData(self, file, tableau_a_imprimer):
        with open(file, 'w') as file:
            for ligne in tableau_a_imprimer:
                file.write(str(ligne))
                file.write('\n')

    # fonction qui va rechercher le jour no1
    def lecturePremierJour(self, fName=r'.\Data\C105CHAB_I6E.txt'):
        fName.replace('\\', '/')
        with open(fName, 'r') as file:
            # pour chaque ligne(ici représentée par lines) dans le fichier
            for lines in file.readlines():
                # si le premier mot de la ligne est un chiffre, alors split de la ligne en mots puis insertion du 1er
                # mot dans la var locale date
                if lines[0].isdigit():
                    words = lines.split()
                    date = words[0]
                    jour = date[0:2]
                    print(jour)
                    while jour >= "01":
                        self.readFile()

    # lecture du placement des canaux par défaut de la class setup
    # def canRead(self, can_source):
    #     return setup.par['can'][can_source]

    # instancie le tableau de sortie remplit initialement de 0 (int) puis remplis avec des valeurs par défaut
    # pour 31j
    def initTableau(self):
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
        self.printData(r'test_out.txt', self.data_int)

    #  fonction qui pour chaque canal var lire les lignes avec le canal correspondant, récupère le jour de la ligne traitée
    #  et log les infos et erreurs
    def conversionData(self):
        #  variable qui va jusqu'à 2 - compte le nmbre de passage de la plage horaire (0100-1200 et 1300-2400)
        #  d'une date selon un canal
        nb_plage_horaire = 0

        can = setup.par.get(str(self.compteur_num))
        print(can)
        for n in can:
            print('----------- ------------- ----------------' + str(n) + '------------ ------------ ----------- -----')
            #  pour chaque lignes dans le tableau data_ascii
            for ligne in self.data_ascii:
                #  si le n° de canal de par['can'] correspond au n° de canal du tableau data_ascii
                if int(ligne[2]) == n:
                    #  récupérer la ligne pointée dans data_ascii et l'attribuer dans la variable data
                    data = ligne
                    print(data)
                    #  récupérer le numéro du jour sur 1 ou 2 digits
                    date = data[0]
                    day = int(date[4:6])
                    print(day)
                    #  appel de la fonction avec paramètres
                    self.conv_LineToCol(data, n, day, nb_plage_horaire)
                    #  incrémentation de la variable
                    nb_plage_horaire += 1
                    #  si la variable nb_plage_horaire est égal à 2, on log et on remet la variable nb_plage_horaire à 0
                    if nb_plage_horaire == 2:
                        logging.info(
                            "le jour " + str(day) + " pour le canal no " + str(n) + " a été inséré dans le "
                                                                                      "tableau de sortie")
                        nb_plage_horaire = 0

                else:
                    print("erreur")
                #     logging.error("le jour " + str(day) + " pour le canal no " + str(compteur) + " est manquant dans le "
                #     " tableau d'entrée")
        self.printData(r'test_out.txt', self.data_int)
        t1 = time.time()
        logging.info('Fin de l application en {0} secondes.'.format(t1 - self.t0))

    #  fonction qui va convertir les données d'un tablea à un autre à l'aide de la fonction  conv_LineToCol
    def conv_LineToCol(self, data, compteur, day, nb_plage_horaire):
        #  instanciation de la variable index à 3 - car c'est à partir de la 4è position que sont les données à traiter
        index = 3
        #  tant que index est inférieur à la longueur du tableau data
        while index < len(data):
            #  attribution de la valeur pointée dans data à la variable nbre
            nbre = int(data[index])

            heure = (index - 3) + 12 * (nb_plage_horaire)
            self.data_int[(day - 1) * 24 + heure][2 + compteur] = nbre
            print(nbre)
            print(index)
            index += 1


if __name__ == '__main__':
    x = CounterM720()
    x.nomFichierALire()
    x.readFile()
    x.conversionData()

    print("---------------\n")

    # print(x.compteur_num)
    # print(x.affect_canal)
    # print(x.nbre_canal)
    # print(x.date_debut)
    # print(x.canRead(2))
    # print(x.lecturePremierJour)
    # print(x.nomFichierALire)
    # print(x.data_ascii)
    # print(x.data_int)
