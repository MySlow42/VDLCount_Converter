"""
Ville de Lausanne - Routes et mobilité
R Cordonier 01/2019
Traitement et conversions des fichiers des compteurs Golden River et MetroCount en un format de sortie normalisé .ASB
Selon le point 7.2 du CDC
Programme principal
"""
import sys
import setup as Set
import counterM720 as M720


def main(argv):
    #global data
    Set.setargs(argv)
    print('traiter: %s' % Set.par['infile'])


if __name__ == '__main__':
    main(sys.argv)
    Set.set_config()
    x = M720.CounterM720()
    x.nomFichierALire(Set.nom_fichier_lire)
    x.readFile()
    x.conversionData()
