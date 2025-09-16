#!/bin/bash
HOST="127.0.0.1"
PORT="5555"

# Liste tous les fichiers *.ia à la racine, en mélange l'ordre
#IA_FILES=($(find . -maxdepth 1 -type f -name "*.py" | shuf))
IA_FILES="neonbot_boss.py"
# Si moins de 8 IA disponibles, on boucle sur la liste
for i in $(seq 1 8); do
    IA_FILE="${IA_FILES[$(( (i-1) % ${#IA_FILES[@]} ))]}"
    NAME="Bot_$i"
    gnome-terminal -- bash -c "
        echo 'Lancement du bot $NAME avec $IA_FILE...';
        python3 \"$IA_FILE\";
        echo 'Bot $NAME terminé (mort ou déconnecté)'; sleep 2
    " &
done
