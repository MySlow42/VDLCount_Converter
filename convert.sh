#!/bin/bash
#╔═══════════════════════════════════╗
#║Crée par Poli                      ║
#╠═══════════════════════════════════╣
#║Fork de MySlow42/VDLCount_Converter║
#╠═══════════════════════════════════╣
#║Ce script permet de convertir un   ║
#║tableau vertical en horizental     ║
#║(ou l'inverse je sais plus)        ║
#╠═══════════════════════════════════╣
#║Initialisé le 28.03.2019           ║
#╚═══════════════════════════════════╝

#╔═══════════════════════════════════════════════════════════════════════
#║ Tout les commentaires auront cette forme
#╚═══════════════════════════════════════════════════════════════════════

#╔═══════════════════════════════════════════════════════════════════════
#║
#╚═══════════════════════════════════════════════════════════════════════

#╔═══════════════════════════════════════════════════════════════════════
#║ Appel de $1 pour la variable positionel (choix du fichier a traiter
#║ (donc sont chemin)
#╚═══════════════════════════════════════════════════════════════════════

Fichier_Traiter=$1

#╔═══════════════════════════════════════════════════════════════════════
#║ Trouver la ligne * channel et garder le nombre de canal
#║ (Petit regex sur le fichier pour récuperer la ligne CHANNELS)
#║ egrep c'est un truc pour executer les regex sur un fichier par exemple
#║ egrep c'est un grep -e (-e dis --extended-regexp) et donc tout du
#║ regex comme ça tu peux l'utiliser aussi
#║ $() permet d'executer la commande rien de bien spécial ^^
#╚═══════════════════════════════════════════════════════════════════════

NombreChannel=$(egrep '^.*\CHANNELS\b.*$' $Fichier_Traiter)

#╔═══════════════════════════════════════════════════════════════════════
#║ Enlever tout jusqu'a un espace après le égale
#║ sed c'est comme re.sub() sous python
#╚═══════════════════════════════════════════════════════════════════════

NombreChannel=$(echo "$NombreChannel" | sed -e 's/.*=//')

#╔═══════════════════════════════════════════════════════════════════════
#║ Maintenant nous allons récupré le site sed va enelver tout après le =
#║ et la deuxième fois enleve les esapces
#╚═══════════════════════════════════════════════════════════════════════

NumeroSite=$(egrep '^.*\SITE\b.*$' $Fichier_Traiter)
NumeroSite=$(echo "$NumeroSite" | sed -e 's/.*=//' | sed 's/ //g')
echo "$NumeroSite"

#╔═══════════════════════════════════════════════════════════════════════
#║ Ici ça sépare chaque numéro et le met dans un array
#║ ça a l'air vraiment compliquer mais IFS c'est un str_split enfaite
#║ et a la fin je récupere la taille de l'array permetant de savoir le
#║ nombre de canaux
#╚═══════════════════════════════════════════════════════════════════════

IFS=', ' read -r -a SplitChannel <<<"$NombreChannel"
ArraySize=${#SplitChannel[@]}

echo "Nous avons $ArraySize canaux a traité"

#╔═══════════════════════════════════════════════════════════════════════
#║ grep pour enlever toutes les lignes ne commancant pas par un numéro
#║ grep -v inverse le sense de matching donc la je cherche tout les
#║ numéro et au lieu de les supprimer je garde que eux (REGEX)
#╚═══════════════════════════════════════════════════════════════════════

data=$(grep -v "^[^0-9]" $Fichier_Traiter)
while read line; do
    i="-1"
    CountData="-1"
    let "LineNumber++"
    echo "LINE: '${line}'"
    IFS=', ' read -r -a SplitData <<<"$line"
    for element in "${SplitData[@]}"; do
        let "i++"
        echo "$i $element"
        if [[ $i == "0" ]]; then
            Date=$element
        elif [[ $i == "2" ]]; then
            Canal=$element
        fi
        if [[ $i -gt "2" ]]; then
            let "CountData++"
            declare Data$CountData="$element"
        fi
    done

    echo "Date $Date"
    echo "Canal $Canal"
    echo "Data0 $Data0"
    echo "Data1 $Data1"
    echo "Data2 $Data2"
    echo "Data3 $Data3"
    echo "Data4 $Data4"
    echo "Data5 $Data5"
    echo "Data6 $Data6"
    echo "Data7 $Data7"
    echo "Data8 $Data8"
    echo "Data9 $Data9"
    echo "Data10 $Data10"
    echo "Data11 $Data11"
    declare -A array$LineNumber
    declare array$LineNumber[0]="$Date"
    declare array$LineNumber[1]="$Canal"
    declare array$LineNumber[2]="$Data0"
done <<<"$data"
