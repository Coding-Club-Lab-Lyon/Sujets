#!/usr/bin/env python3

#import random
#mots = ["casserole", "cuillere", "patate", "souris"]
#solution = random.choice(mots)

solution = "hello"
tours = 10
affichage = ""
lettres_trouvees = ""

for l in solution:
    affichage = affichage + "_ "

print(">> Bienvenue dans le pendu <<\n")

while tours > 0:
    print("Mot à deviner : ", affichage)
    proposition = input("proposez une lettre : ")[0:1].lower()

    if proposition in solution:
        lettres_trouvees = lettres_trouvees + proposition
        print("-> Bien vu!")
    else:
        tours = tours - 1
        print("-> Nope\n")
        print("Il te reste ", tours, " tentative(s)\n")

    affichage = ""
    for lettre in solution:
        if lettre in lettres_trouvees:
            affichage += lettre + " "
        else:
            affichage += "_ "

    if "_" not in affichage:
        print(">>> Gagné! <<<\n")
        break

print("* Fin de la partie *")