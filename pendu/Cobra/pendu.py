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

    if "_" not in mot:
        print(">>> Gagné! <<<")
        break
    else:
        print(message)
        proposition = input("Proposez une lettre : ")[0:1].lower()

    if proposition in lettres_trouvees:
        message = "Lettre déjà proposée"
        continue
    elif proposition in solution:
        lettres_trouvees = lettres_trouvees + proposition
        message = "Lettre correcte"
    else:
        erreurs += 1
        pendu.set_step(erreurs)
        message = "Lettre incorrecte"

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
    print(">>> Perdu! <<<")
    print(">>> Le mot était : " + solution + " <<<")


print("* Fin de la partie *")