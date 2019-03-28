"""
Ville de Lausanne - Routes et mobilité
R Cordonier 01/2019
Traitement et conversions des fichiers des compteurs Golden River et MetroCount en un format de sortie normalisé
Selon le point 7.2 du CDC
Programme principal
"""
import setup as Set
import countObjects as Count
import readM720 as M720
import sys, os, logging

data = []

def main(argv):
    global data
    Set.setargs(argv)
    print('traiter: %s' % Set.par['infile'])
    M720.ReadM720.readFile(Set.par['infile'])
    M720.ReadM720.__repr__()

















if __name__ == '__main__':
    main(sys.argv)