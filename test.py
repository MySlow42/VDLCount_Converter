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

if __name__ == '__main__':
    import sys

    x = test()
    #x.readFile(r'.\Data\C105CHAB_I6E.txt')
    x.readFile()

    print(x.readFile)
    print('blabla')