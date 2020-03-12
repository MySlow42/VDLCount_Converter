import logging

NAME = 'CountConverter.py'
VERSION = '1.2'

#  paramètre pour le logger
logging.basicConfig(filename='fichier.log', level=logging.DEBUG,
                    format='%(asctime)s -- %(levelname)s -- %(message)s')
logging = logging.getLogger('setup')

logging.info('Démarrage de {0} -- version {1}'.format(NAME, VERSION))

fichier_config = r'\lausanne.ch\DATA\430\Groups\5_Mobilite\Mobilite\4_Comptages\Permanents\Données_brutes\config.txt'
par = []

class test:


    def Test(self):
        with open(fichier_config, 'r') as file:
            for lignes in file.readlines():
                sp = lignes.split('#')[0]
                sp = sp.replace('\n', '')
                sp = sp.split('=')
                if sp[0] == "repertoire":
                    par['path file'] = str(sp[1]).encode('utf-8').decode('ansi')
        print(par['path file'])


if __name__ == '__main__':
    import sys

    x = test()
    # x.readFile(r'.\Data\C105CHAB_I6E.txt')
    # x.readFile()
    # x.nomFichierALire()
    #x.stringConcatenation()
    x.Test()

    # print(x.nomFichierALire)
