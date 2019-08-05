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
    def readFile(self, fName=r'.\Data\C105CHAB_I6E.txt'):
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

    def stringConcatenation(self):
        a = 'hola'
        b = 'que tal?'
        c = 7
        d = 3

        print(a + ' ' + b) #hola que tal?
        print(c + d) #10
        print(a + str(d)) #hola3

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

    def nomFichierALire(self, nom_premier_fichier=r'bka\bla\blo\Data\C105CHAB_I67.txt'):
        nom_premier_fichier.replace('\\', '/')
        liste_nom = []
        nom_fichier = nom_premier_fichier[:-6]
        dizaine_ext_incr = nom_premier_fichier[-6:-5]
        unit_ext_incr = nom_premier_fichier[-5:-4]
        liste_nom.append(nom_premier_fichier)
        nb_fich = 0
        array = ['1','2','3','4','5','6','7','8','9','0']
        d = dizaine_ext_incr 

        while nb_fich < 5:
            print(str(unit_ext_incr) + ' début')
            #Dans le cas où l'unité est un entier
            if str(unit_ext_incr) in array:
                #isinstance(unit_ext_incr, int):
                print(str(unit_ext_incr) + ' unité')
                u = unit_ext_incr
                u = ord(str(u))  # retourne la valeur correspondante en ASCII
                u += 1

                print(u)
                if u > ord('9'): # retourne la valeur de 9 en ASCII
                    u = 'A'
                    print('passe par là bordel!!')
                # chr(u)
                else:
                    u = chr(u)
                print('je suis passé par làààà')
            else:
                # Dans le cas où l'unité est un string
                unit_ext_incr = unit_ext_incr.upper()
                u = chr(ord(unit_ext_incr) + 1)
                if u > chr(ord('Z')):
                    u = 0
                    print(str(u) + 'String u valeur en ASCII > 0')
                    if isinstance(dizaine_ext_incr, int):
                        print(str(dizaine_ext_incr) + 'dizaine')
                        d = ord(dizaine_ext_incr)  # retourne la valeur correspondante en ASCII
                        print(str(d) + 'int d valeur en ASCII')
                        d += 1
                        if d > 9:
                            d = 'A'
                        # chr(d)
                        print(str(d) + 'int d valeur en ASCII +1 > A')
                    else:
                        dizaine_ext_incr = dizaine_ext_incr.upper()
                        d = chr(ord(dizaine_ext_incr) + 1)
                        if d > chr(ord('Z')):
                            d = 0
                        print(str(d) + 'String d valeur en ASCII > 0')

            unit_ext_incr = u
            dizaine_ext_incr = d
            nom = nom_fichier + str(d) + str(u)
            print(d, u)
            liste_nom.append(nom)
            nb_fich += 1
            print(liste_nom)


    def Test(self):
        words = ['190303', '0100', '3', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        for i in words[3:]:
            print(i)
        if(len(set(words[3:]))==1):
            print("passe ici bordel")



if __name__ == '__main__':
    import sys

    x = test()
    # x.readFile(r'.\Data\C105CHAB_I6E.txt')
    # x.readFile()
    # x.nomFichierALire()
    #x.stringConcatenation()
    x.Test()

    # print(x.nomFichierALire)
