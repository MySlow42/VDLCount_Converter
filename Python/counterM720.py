"""
Ville de Lausanne - Routes et mobilité
R Cordonier 01/2019
Traitement et conversions des fichiers des compteurs Golden River et MetroCount en un format de sortie normalisé .ASB
Selon le point 7.2 du CDC
recherche les fichiers pour un mois de comptage à lire puis traîtement des fichiers.
Le traitement de ces fichiers incluent 2 tableaux intermédiraires, dans un premier temps, un tableau qui stockera les
données en ASCII avant d'être convertie en données numériques. Le format de date diffère à l'entrée comparé à la sortie
"""
# Import des modules nécessaires
import time
import sys
import os
import os.path
import logging
import numpy as np
import setup


# coding: utf8

class CounterM720:
    #  variables globales
    liste_nom = []
    jour = ''
    date = ''

    #  paramètre pour le logger
    logging.basicConfig(handlers=[logging.FileHandler('fichier.log', 'w', 'utf-8')], level=logging.DEBUG,
                        format='%(asctime)s -- %(levelname)s -- %(message)s')
    #  appel du logger du nom de "counterM720"
    logging = logging.getLogger('setup')
    t0 = time.time()

    """ constructeur qui fait le lien avec les variables statiques et locales
     Prend en paramètre les variables utiles à la classe"""

    def __init__(self, nbrecan=0, ddebut=0, ):
        self.compteur_num = ''
        self.nbre_canal = nbrecan
        self.affect_canal = []
        self.date_debut = ddebut
        self.data_ascii = []
        # var qui correspond au premier jour à traiter
        self.premier_jour_a_chercher = "01"

    # fonction qui va lire le fichier,contenant le 1er jour, inséré par l'user et déterminer les autres fichiers consécutifs  à lire
    # le r avant le pathfile va empêcher le backslash d'être interprété comme caractère d'échappement en le doublant
    def nomFichierALire(self, nom_premier_fichier):
        logging.info('Nom du fichier inséré: {0}'.format(nom_premier_fichier))
        nom_premier_fichier = nom_premier_fichier.replace('\\', '/')  # remplace les \\ en /
        nom_premier_fichier = nom_premier_fichier.upper()  # mise en maj de la chaîne
        path_nom_fichier = nom_premier_fichier[:-6]  # tronquage du pathfile pour obtenir que le nom du fichier
        premier_char_extension = nom_premier_fichier[-5:-4]  # récupération du 1er caractère qui devra être incrémenter
        deuxieme_char_extension = nom_premier_fichier[-6:-5]  # récupération du 2nd caractère qui devra être incrémenter
        extension = nom_premier_fichier[-4:]  # récupération de l'extension
        print(self.liste_nom)
        self.liste_nom.append(nom_premier_fichier)  # insertion du 1er pathfile (donné par l'user)
        nb_fich = 0  # l'index du premier fichier est de 0

        # tant que le nbre de fichier est en dessous de 6
        while nb_fich < 6:
            premier_char_extension = CounterM720.incr09az(self,
                                                          premier_char_extension)  # appel de la fonction incr09az avec u en paramètre
            if premier_char_extension == '0':  # si u est egal à 0
                deuxieme_char_extension = CounterM720.incr09az(self,
                                                               deuxieme_char_extension)  # appel de la fonction incr09az avec d en paramètre

            nom = path_nom_fichier + str(deuxieme_char_extension) + str(
                premier_char_extension) + extension  # contruction du nouveau nom de fichier avec extension
            print(deuxieme_char_extension, premier_char_extension)
            self.liste_nom.append(nom)  # insertion du nouveau nom de fichier dans la liste
            nb_fich += 1  # incrémentation de la var
            print(self.liste_nom)

    # fonction qui prend en paramètre le premier ou le second caractère de l'extension du fichier
    # exemple C036TUN_I0B - extension = 0B
    def incr09az(self, charFile):
        if charFile.isdecimal():  # si le caractère est un décimal
            if charFile == '9':  # s'il est égal à 9 retourner A
                return 'A'
            else:
                return chr(ord(
                    charFile) + 1)  # sinon traite les valeurs de 0 à 8
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
        iteration_data_ascii: int = 0  # variable qui contient la date du fichier d'entrée
        jour_1 = False  # flage de recherche du 1er jour à chercher
        print(self.liste_nom[index_liste_nom])
        # Pour chaque nom dans la liste de fichiers à traiter
        for fName in self.liste_nom:
            # Teste si le fichier existe et peut s'ouvrir et traite l'erreur
            try:
                with open(fName, 'r') as file:
                    pass

            except FileNotFoundError:
                if nb_fichiers_lus == 0:
                    so = "Erreur 01! Le 1er fichier ({0}) n' pas pu être ouvert. Fin du programme. Veuillez contrôler " \
                         "que le fichier existe sous ce nom.".format(fName)
                    print(so)
                    logging.error(so)
                    sys.exit()

                else:
                    so = "Le fichier {0} n' pas pu être ouvert et ne sera donc pas traité. Veuillez contrôler que le " \
                         "fichier existe sous ce nom.".format(fName)
                    print(so)
                    logging.info(so)
            else:
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

                            # si le nbre de fichiers lus est suppérieur ou égal à 0
                        if nb_fichiers_lus >= 0:
                            # si le premier élément dans le tableau est un chiffre
                            # alors récupération des 2 derniers chiffres et les attribuer à la variable jour
                            if lines[0].isdigit():
                                words = lines.split()
                                date = words[0]
                                self.jour = date[0:2]
                                print(self.jour)

                                # teste si la ligne du compteur est à 0
                                if words[3:].count('0') == 12:
                                    so = "La Ligne en date du {} à {} pour le canal {} est entièrement à 0.".format(
                                        self.jour, words[1:2], words[2:3])
                                    print(so)
                                    logging.info(so)

                                if jour_1 == False:  # premier jour du mois pas encore trouvé
                                    # si le premier mot de la ligne est un chiffre, alors split de la ligne en mots puis
                                    # insertion des données de comptage dans le tableau intermédiaire ascii

                                    if self.jour == self.premier_jour_a_chercher:
                                        print(self.premier_jour_a_chercher)
                                        jour_1 = True
                                    self.date_debut = date
                                    print(date)

                                # s'il y a déjà un premier jour alors on arrête la boucle
                                if self.jour == self.premier_jour_a_chercher and jour_1 and nb_fichiers_lus > 0:
                                    break

                                if jour_1:
                                    self.data_ascii.append(words)
                                    # du moment que la var iteration_data_ascii est inférieure ou égale à la longeure du tab
                                    # data alors prendre 1e mot de la ligne (la date) et l'injecter dans la var
                                    # iterationDate
                                    iterationDate = self.data_ascii[iteration_data_ascii][0]
                                    # conversion de 2 carcatères (sélectionnés par des []) de la var string iterationDate
                                    # en int puis multiplication de ceux-ci selon la position souhaitée pour obtenir le
                                    # format de sortie désiré - format entrée AAMMJJ format sortie JJMMAA
                                    iterDateFormatSortie = (iterationDate[-2:]) + (iterationDate[-4:-2]) + (
                                        iterationDate[:2])
                                    # Insertion de la var iterDateFormatSortie dans la première position de chaque ligne du
                                    # tab data
                                    self.data_ascii[iteration_data_ascii][0] = iterDateFormatSortie
                                    self.date = iterDateFormatSortie
                                    # incrémentation de la var iteration_data_ascii
                                    print(self.data_ascii[iteration_data_ascii][0])
                                    iteration_data_ascii += 1

            # imprime les données avec la date dans le bon format dans le fichier de sortie test_in.txt
            self.printData(r'test_in.txt', self.data_ascii)
            # impressime fin du traitement + nom du fichier traiter
            print('Fin du traitement du fichier' + self.liste_nom[index_liste_nom])
            # Incrémente les valeurs de 1
            index_liste_nom += 1
            nb_fichiers_recus += 1
            nb_fichiers_lus += 1
        if not jour_1:
            so = "Erreur 20! Pas de jour no 1 trouvé. Arrêt du programme. Veuillez vérifier l'exatitude de vos fichiers."
            print(so)
            logging.error(so)
            sys.exit()
        else:
            # Appel de la fonction suivante
            self.initTableau()

    # fonction qui imprime les données d'un tableau dans un fichier externe
    def printData(self, file, tableau_a_imprimer):
        with open(file, 'w') as file:
            for ligne in tableau_a_imprimer:
                file.write(str(ligne))
                file.write('\n')

    # fonction qui va rechercher le jour no1
    def lecturePremierJour(self, fName=setup.par['infile']):
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
                    while jour >= self.premier_jour_a_chercher:
                        self.readFile()

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
            self.data_int[i][0] = self.compteur_num
            # self.data_int[i][1] = self.date
            i += 1
        self.printData(r'test_out.txt', self.data_int)

    #  fonction qui pour chaque canal var lire les lignes avec le canal correspondant, récupère le jour de la ligne traitée
    #  et log les infos et erreurs
    def conversionData(self):
        #  variable qui va jusqu'à 2 - compte le nmbre de passage de la plage horaire (0100-1200 et 1300-2400)
        #  d'une date selon un canal
        nb_plage_horaire = 0

        if self.compteur_num == '':
            so = "Le numéro de compteur n'a pas été trouvé. Vérifiez que le 1er fichier ( {0} ) existe sous ce nom ou " \
                 "insérez le n° de compteur.".format(setup.par['infile'])
            print(so)
            logging.info(so)
            self.compteur_num = input("Entrer ici le numéro du compteur ou interrompez le programme: ")
            so = "Le numéro de compteur inséré par l'utilisateur est: " + self.compteur_num
            print(so)
            logging.info(so)
        else:
            with open(setup.fichier_config, 'r') as file:
                for lignes in file.readlines():
                    if str(self.compteur_num) in lignes:
                        sp = lignes.replace('\n', '')
                        sp = sp.split('=')
                        sp[1] = sp[1].split(',')
                        c = 0
                        sp[1] = [int(i) for i in sp[1]]
                        print("sp[1]" + str(sp[1]))

            can = sp[1]
            print("num de can est: " + str(can))

        # tests si tous les canaux sont à 0
        if can.count(0) > 5:
            so = 'Erreur 21! Le canal ' + str(
                self.compteur_num) + ' ne contient que des 0. Veuillez vérifier le fichier ' \
                                     'de config. Arrêt du programme.'
            print(so)
            logging.error(so)
            sys.exit()

        # else:
        for n in can:
            print('----------- ------------- ------------' + str(n) + '------------ ------------- ---------------')
            if n > 6:
                so = 'Le canal ' + str(self.compteur_num) + ' a une entrée à ' + str(n) + ' qui ne sera pas ' \
                                                                                          'traitée. Veuillez ne ' \
                                                                                          'pas dépasser 6 entrées ' \
                                                                                          'par canal.'
                print(so)
                logging.info(so)
            else:
                #  pour chaque lignes dans le tableau data_ascii
                for ligne in self.data_ascii:
                    #  si le n° de canal de par['can'] correspond au n° de canal du tableau data_ascii
                    if int(ligne[2]) == n:
                        #  récupérer la ligne pointée dans data_ascii et l'attribuer dans la variable data
                        data = ligne
                        #  récupérer le numéro du jour sur 1 ou 2 digits
                        date = data[0]
                        day = int(date[4:6])
                        #  appel de la fonction avec paramètres
                        self.conv_LineToCol(data, n, day, nb_plage_horaire)
                        #  incrémentation de la variable
                        nb_plage_horaire += 1
                        #  si la variable nb_plage_horaire est égal à 2, on log et on remet la variable nb_plage_horaire à 0
                        if nb_plage_horaire == 2:
                            logging.debug(
                                "Le jour " + str(day) + " pour le canal no " + str(n) + " a été inséré dans le "
                                                                                        "tableau de sortie")
                            nb_plage_horaire = 0

                    else:

                        pass

        # Insère l'en-tête du fichier de sortie
        i = 0
        while i < 9:
            np.insert(self.data_int, i, i + 1)
            i += 1

        self.printData(r'test_out.txt', self.data_int)
        self.insert_repertoire(self.date_debut)
        t1 = time.time()
        logging.info('Fin de l application en {0} secondes.'.format(t1 - self.t0))
        sys.exit()

    #  fonction qui va convertir les données du tableau ascii au numérique à l'aide de la fonction  conv_LineToCol qui
    #  prend en paramètre le tableau de données à convertir, le no du compteur, le jour concerné et de quelle plage
    #  horaire il s'agit
    def conv_LineToCol(self, data, no_compteur, day, nb_plage_horaire):
        #  instanciation de la variable index à 3 - car c'est à partir de la 4è position que sont les données à traiter
        index = 3
        #  tant que index est inférieur à la longueur de la ligne du tableau data
        while index < len(data):
            #  attribution de la valeur pointée dans data à la variable nbre
            try:
                nbre = int(data[index])

            except ValueError:
                so = "Le caractère inséré " + str(data[index]) + " en date du " + str(day) + " n'est pas un entier. " \
                                                                                             "Il sera remplacé par " \
                                                                                             "un 0 dans le fichier " \
                                                                                             "de sortie."
                print(so)
                logging.info(so)
                nbre = 0
                heure = (index - 3) + 12 * (nb_plage_horaire)
                self.data_int[(day - 1) * 24 + heure][2 + no_compteur] = nbre
                index += 1

            else:
                nbre = int(data[index])
                heure = (index - 3) + 12 * (nb_plage_horaire)
                self.data_int[(day - 1) * 24 + heure][2 + no_compteur] = nbre
                index += 1

    # Va créer le fichier de l'année et du mois concernant si pas existant et y insérer el fichier de sortie
    def insert_repertoire(self, date_debut):
        # Instanciation variables
        # date_debut sous format jjmmaa
        annee = "20" + str(date_debut[4:])
        mois = date_debut[2:4]
        tab_mois = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Aout', 'Septembre', 'Octobre',
                    'Novembre', 'Décembre']
        repertoire = setup.par['path file']
        logging.info(repertoire)

        repertoire = os.path.join(repertoire, annee)
        repertoire = os.path.join(repertoire, str(mois) + " " + tab_mois[int(mois) - 1])
        # Test si le chemin du dossier existe
        if not os.path.exists(repertoire):
            os.makedirs(repertoire)
        name = (str(self.compteur_num))

        # Insertion des 0 avant le nom du fichier et définition de l'extension en .ABS
        while len(name) < 8:
            name = '0' + name
        name = name + '.ASB'

        # Définition du chemin de fichier
        file = os.path.join(repertoire, name)

        # Ouvrture du fichier en écriture et insertion des données de sortie
        with open(file, 'w') as file:
            for ligne in self.data_int:
                file.write(str(ligne))
                file.write('\n')

        # Affiche un message avant de fermer la fenêtre
        if input("Cette fenêtre se fermera dès que vous aurez cliquer sur Q. Veuillez vérifier le fichier de "
                 "log qui se trouve à l'emplacement du programme.") == "Q" or "q":
            pass


if __name__ == '__main__':
    x = CounterM720()
    x.nomFichierALire(setup.nom_fichier_lire)
    x.readFile()
    x.conversionData()

    print("---------------\n")
