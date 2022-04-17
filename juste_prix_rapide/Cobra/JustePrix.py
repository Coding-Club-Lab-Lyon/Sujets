import random

lots = [{
        "name" : "Ecer Gaming",
        "price" : random.randint(180, 230)
    },
    {
        "name" : "Nantendo Swatch",
        "price" : random.randint(250, 320)
    },
    {
        "name" : "NSA Gaming",
        "price" : random.randint(1000, 1200)
    },
    {
        "name" : "Somsing QLED",
        "price" : random.randint(1000, 1500)
    },
    {
        "name" : "JPL PoomPox",
        "price" : random.randint(100, 180)
    }]

print("Bienvenue dans le jeu du Juste Prix")
lot = random.choice(lots)
print("Aujourd'hui, le lot à gagner est \"{}\"".format(lot["name"]))
user_price = 0
while user_price != lot["price"]:
    user_price = int(input("Entrez un prix: "))
    if user_price > lot["price"]:
        print("C'est moins !")
    elif user_price < lot["price"]:
        print("C'est plus !")
    else:
        print("Bravo, vous avez trouvé le juste prix !")
