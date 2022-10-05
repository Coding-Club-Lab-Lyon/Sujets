#!/usr/bin/env python3
import random
import os
from cc_pendu.ascii import Pendu

pendu = Pendu()

with open("mots.txt") as word_file:
    liste_de_mots = word_file.readlines()
    solution = random.choice(liste_de_mots).replace("\n", "")

erreurs = 0
lettres_trouvees = ""

mot = ""
for l in solution:
    mot = mot + "_ "

message = ""

while erreurs < 11:
    os.system("clear")
    print(pendu)
    print(mot)
    print("")

    # écrit ton code dans cette partie :
    # entre cette ligne 






    # et celle-ci

    mot = ""
    for lettre in solution:
        if lettre in lettres_trouvees:
            mot += lettre.upper() + " "
        else:
            mot += "_ "

if (erreurs == 11):
    os.system("clear")
    print(pendu)
    print(mot)
    print("")
    
    # écrit le message de défaite ici

print("* Fin de la partie *")