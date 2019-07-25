"""
Ville de Lausanne - Routes et mobilité
R Cordonier 01/2019
Traitement et conversions des fichiers des compteurs Golden River et MetroCount en un format de sortie normalisé
Selon le point 7.2 du CDC
setup
"""
import sys, os
import logging

# import logging



#  paramètre pour le logger
logging.basicConfig(filename='test_log.log', level=logging.DEBUG,
                    format='%(asctime)s -- %(levelname)s -- %(message)s')
logging = logging.getLogger('spam')

NAME = 'CountConverter.py'
VERSION = '0.1'
ERR_ARGS = 1
ERR_INFILE = 2
ERR_CONFIG = 3
ERR_OUTFILE = 4
ERR_FORMAT = 5
logging.info('Démarrage de {0} -- version {1}'.format(NAME, VERSION))

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
    try:
        with open(fichier, 'r') as file:
            pass
    except IOError:
        print("Erreur! Le fichier {0} n' pas pu être ouvert. Fin du programme. Veuillez contrôler que le"
                      " fichier existe sous ce nom.".format(fichier))
        logging.error("Erreur! Le fichier {0} n'a pas pu être ouvert. Fin du programme. Veuillez contrôler que le"
                      " fichier existe sous ce nom.".format(fichier))
        sys.exit()
    else: #faire avec un raise
        if os.path.getsize(fichier) == 0:
            print("Erreur! Le fichier {0} est vide. Fin du programme. Veuillez contrôler que le"
                          " fichier.".format(fichier))
            logging.error("Erreur! Le fichier {0} est vide. Fin du programme. Veuillez contrôler que le"
                          " fichier.".format(fichier))
            sys.exit()
        else:
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

            # for valeurs in par.values():
            #     for valeur in valeurs:
            #         print(valeur)

            print('nbre de 0 dans le dictionnaire par: ' + str(sum(value == 0 for value in par.values())))
            # print('le fichier est grand comme: ' + str(os.path.getsize(fichier)))


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
