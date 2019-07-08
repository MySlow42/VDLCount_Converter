"""
Ville de Lausanne - Routes et mobilité
R Cordonier 01/2019
Traitement et conversions des fichiers des compteurs Golden River et MetroCount en un format de sortie normalisé
Selon le point 7.2 du CDC
setup
"""
import sys

# import logging



# class MonLogging:
#     def __init__(self):
#         logger = logging.getLogger()
#         logging.basicConfig(level=logging.debug, format='%(levelname)-8s %(message)s', filename='test.log', filemode='w')
#         logging.info("fichier test.log créé dans setup")

NAME = 'CountConverter.py'
VERSION = '0.1'
ERR_ARGS = 1
ERR_INFILE = 2
ERR_CONFIG = 3
ERR_OUTFILE = 4
ERR_FORMAT = 5
# MonLogging.logging.info('test1')

par = {}
par['infile'] = '.\Data\C105CHAB_I6s.txt'
par['par défaut'] = [1, 2, 3, 0, 0, 0]


def count_help():
    # Définit l'aide en ligne
    print('Utilisation: \n'
          '{0} <nom de fichier> [/t: <type>] \n'
          'Avec:\n'
          '<nom de fichier>: fichier brut a traiter\n'
          'Type: 1-M720, 2-MetroCount, 3-EcoCounter, 4-Scala'.format(NAME))


def set_config():
    fichier = r'.\Data\config.txt'
    # print("le no du compteur est: " + compteur)
    with open(fichier, 'r') as file:
        for lignes in file.readlines():
            sp = lignes.split('#')[0]
            sp = sp.replace('\n', '')
            sp = sp.split('=')
            if len(sp) == 2:
                sp[1] = sp[1].split(',')
                c = 0
                for no in sp[1]:
                    sp[1][c] = int(sp[1][c])
                    c += 1
                par[sp[0]] = sp[1]
                print(sp[0])
    for i in par.get('135'):
        print(i)


def setargs(argv):
    if len(argv) > 1:
        par["infile"] = argv[1]

    if len(argv) > 2:
        par["type"] = argv[2]

    if len(argv) > 1 and ('/?' in argv[1]):
        count_help()
        sys.exit(ERR_ARGS)


if __name__ == '__main__':
    print('Nom: {0}\nVersion: {1}'.format(NAME, VERSION))
    setargs(sys.argv)
    set_config()
    print(par)
