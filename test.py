import numpy as np

class test:
    def ReadConfig(self, fichier=r'.\Data\config.txt', can_ascii='1'):
        with open(fichier, 'r') as file:
            for lines in file.readlines():
                if lines.startswith(can_ascii):
                    words = lines.split()
                    try:
                        can_int = (int(words[1]))
                    except ValueError:
                        print("La valeur recherchée dans le fichier {0} n'est pas un chiffre".format(fichier))
                    else:
                        return can_int

    @classmethod
    def readFile(self, fName = r'.\Data\C105CHAB_I6E.txt'):
        fName.replace('\\', '/')
        # ouverture du fichier en lecture, instanciation de la variable "iteration" qui nous servira d'index
        with open(fName, 'r') as file:

            # pour chaque ligne(ici représentée par lines) dans le fichier
            for lines in file.readlines():
                if not lines[0].isdigit():
                    i += 1
                    print('entered if')
                    print(i)
                else:
                    print('sortie')
                    break


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
                    # while jour >= "01":
                      #  readFile()


    def nomFichierALire(self, nom_premier_fichier=r'bka\bla\blo\Data\C105CHAB_I6E.txt'):
        nom_premier_fichier.replace('\\', '/')
        liste_nom = []
        lien = nom_premier_fichier.split('\\')
        print(lien)
        nom_complet = lien[4:5]
        nom_fichier = str(nom_complet)[:-10]
        print(nom_fichier)
        ext_incr = str(nom_complet)[-8:-6]
        print(ext_incr)
        nb_fich = 0
        i = 0
        #liste_nom = liste_nom + nom_premier_fichier
        while nb_fich < 1:
            if ext_incr[0:1].isdigt:
                print(ext_incr[0:1])
                c = ord(ext_incr[0:1]) # retourne la valeur correspondante en ASCII
                print(c)
                c += 1
                nb_fich +=1
                #chr(c)
                print(c)
            else:
                c = chr(ord(ext_incr) + 1)
                print(c)


if __name__ == '__main__':
    import sys

    x = test()
    #x.readFile(r'.\Data\C105CHAB_I6E.txt')
    # x.readFile()
    x.nomFichierALire()

    print(x.nomFichierALire)
    print('blabla')