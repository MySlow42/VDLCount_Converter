"""
Ville de Lausanne - Routes et mobilité
R Cordonier 01/2019
Traitement et conversions des fichiers des compteurs Golden River et MetroCount en un format de sortie normalisé .ASB
Selon le point 7.2 du CDC
setup
"""
import sys, os
import logging


#  param�tre pour le logger
logging.basicConfig(filename='fichier.log', level=logging.DEBUG,
                    format='%(asctime)s -- %(levelname)s -- %(message)s')

NAME = 'CountConverter.py'
VERSION = '1.2'
ERR_ARGS = 1
ERR_INFILE = 2
ERR_CONFIG = 3
ERR_OUTFILE = 4
ERR_FORMAT = 5
logging.info('Démarrage de {0} -- version {1}'.format(NAME, VERSION))

par = {}
par['infile'] = input("Veuillez insérer le nom du fichier qui contient le premier jour à traiter: ")
par['path file'] = r'./Data/'
par['path log file'] = r'\\lausanne.ch\DATA\6A0\Apps\applications\Count_Converter\Python\fichier.log'
par['infile'] = str(par['path file']) + str(par['infile'])
par['par défaut'] = [1, 2, 3, 0, 0, 0]
nom_fichier_lire = par['infile']
fichier_config = r'.\Data\config.txt'
#nom_fichier_log = r'.\Data\fichier.log'

#  param�tre pour le logger
logging.basicConfig(filename='fichier.log', level=logging.DEBUG,
                    format='%(asctime)s -- %(levelname)s -- %(message)s')
# Appel du logger "setup"
logging = logging.getLogger('setup')

logging.info('Démarrage de {0} -- version {1}'.format(NAME, VERSION))

print("log ok")

def count_help():
    # D�finit l'aide en ligne
    print('Utilisation: \n'
          '{0} <nom de fichier> [/t: <type>] \n'
          'Avec:\n'
          '<nom de fichier>: fichier brut a traiter\n'
          'Type: 1-M720, 2-MetroCount, 3-EcoCounter, 4-Scala'.format(NAME))


# noinspection LossyEncoding
def set_config():
    #fichier = r'.\Data\config.txt'
    # test si le fichier est lisible sinon erreur et log
    try:
        with open(fichier_config, 'r') as file:
            pass
    except IOError:
        so = "Erreur 01! Le fichier {0} n' pas pu être ouvert. Fin du programme. Veuillez contrôler que le fichier existe " \
             "sous ce nom.".format(fichier_config)
        print(so)
        logging.error(so)
        sys.exit()
    else:
        #test si le fichier est vide sinon erreur et log
        if os.path.getsize(fichier_config) == 0:
            so = "Erreur 02! Le fichier {0} est vide. Fin du programme. Veuillez contrôler le fichier.".format(fichier_config)
            print(so)
            logging.error(so)
            sys.exit()
        else:
            with open(fichier_config, 'r', encoding='utf8') as file:
                for lignes in file.readlines():
                    sp = lignes.split('#')[0]
                    sp = sp.replace('\n', '')
                    sp = sp.split('=')
                    if sp[0] == "repertoire":
                        par['path file'] = str(sp[1])

                    elif sp[0] == "fichierLog":
                        par['path log file'] = str(sp[1])
                    else:
                        if len(sp) == 2:
                            sp[1] = sp[1].split(',')
                            c = 0
                            for no in sp[1]:
                                sp[1][c] = int(sp[1][c])
                                c += 1
                            par[sp[0]] = sp[1]

            print('nbre de 0 dans le dictionnaire par: ' + str(sum(value == 0 for value in par.values())))

# fonction qui va setter les arguments passés en paramètre , dans le tableau par[]
def setargs(argv):
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
