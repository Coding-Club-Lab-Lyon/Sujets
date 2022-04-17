import random
import time


Products = {
    "Ecran" : {
        "name" : "Ecer Gaming",
        "price" : random.randint(180, 230)
    },
    "Console" : {
        "name" : "Nantendo Swatch",
        "price" : random.randint(250, 320)
    },
    "Unité centrale" : {
        "name" : "NSA Gaming",
        "price" : random.randint(1000, 1200)
    },
    "Télévision" : {
        "name" : "Somsing QLED",
        "price" : random.randint(1000, 1500)
    },
    "Enceinte" : {
        "name" : "JPL PoomPox",
        "price" : random.randint(100, 180)
    },
}

Dialogue = [
    "",
    "Voix-off : Bonjour et bienvenue au Good Price, avec pour présentateur, Vincent FAIGAF !",
    "Vincent Faigaf : BIP BIP",
    "Le public : OUAIIIIIIS !",
    "Vincent Faigaf : Et on commence tout de suite par la présentation de nos candidats !",
    "Notre premier candidat est : ",
    "Il affrontera : ",
    "Nous allons tout de suite commencer avec le premier produit.",
]


def CustomPrint(text, sleep_time):
    print(text)
    time.sleep(sleep_time)

def StoryTeller():
    for phrase in Dialogue:
        CustomPrint(phrase, 2)

def PlayerTurnVerification(valuePlayer, price, nextPlayerName):
    if valuePlayer < price:
        print("C'est plus ! Au tour de " + nextPlayerName)
    if valuePlayer > price:
        print("C'est moins ! Au tour de " + nextPlayerName)

def RegisterPlayer(player1, player2):
  Dialogue[5] += player1
  Dialogue[6] += player2

def Main():
    playerOne = input("Comment vous appelez vous ? (Premier joueur) : ")
    playerTwo = input("Comment vous appelez vous ? (Second joueur) : ")
    valuePlayerOne = 0
    valuePlayerTwo = 0
    nb_product = random.choice(list(Products.keys()))
    product = Products.get(nb_product)
    price = product.get("price")

    RegisterPlayer(playerOne, playerTwo)
    StoryTeller()

    print("Vous devez trouver le prix de ce produit : ", product.get("name"))

    while valuePlayerOne != price or valuePlayerTwo != price:
        valuePlayerOne = int(input(playerOne + " entrez un nombre : "))
        PlayerTurnVerification(valuePlayerOne, price, playerTwo)
        if (valuePlayerOne == price):
            print(playerOne + " a gagné !")
            break
        valuePlayerTwo = int(input(playerTwo + " entrez un nombre : "))
        PlayerTurnVerification(valuePlayerTwo, price, playerOne)
        if (valuePlayerTwo == price):
            print(playerTwo + " a gagné !")
            break

Main()