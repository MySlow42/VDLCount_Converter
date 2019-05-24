"""
Ville de Lausanne - Routes et mobilité
R Cordonier 01/2019
Traitement et conversions des fichiers des compteurs Golden River et MetroCount en un format de sortie normalisé
Selon le point 7.2 du CDC
setup
"""
import sys

import logging

# import readM720

class MonLogging:
    # def __init__(self):
    logging.basicConfig(level=logging.debug, format='%(levelname)-8s %(message)s', filename='test.log', filemode='w')

NAME = 'CountConverter.py'
VERSION = '0.1'
ERR_ARGS = 1
ERR_INFILE = 2
ERR_CONFIG = 3
ERR_OUTFILE = 4
ERR_FORMAT = 5
# MonLogging.logger.info('test1')

par = {}
par['infile'] = '.\Data\C105CHAB_I6E.txt'
par['can'] = [0, 1, 2, 3, 4, 5, 6]


def count_help():
    # Définit l'aide en ligne
    print('Utilisation: \n'
          '{0} <nom de fichier> [/t: <type>] \n'
          'Avec:\n'
          '<nom de fichier>: fichier brut a traiter\n'
          'Type: 1-M720, 2-MetroCount, 3-EcoCounter, 4-Scala'.format(NAME))


def set_config(fichier=r'.\Data\config.txt'):
    with open(fichier, 'r') as file:
        for lignes in file.readlines():
            sp = lignes.split('#')[0]
            sp = sp.split('=')
            if len(sp) == 2:
                par[sp[0].strip()] = file.close()


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
    print(par)
