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