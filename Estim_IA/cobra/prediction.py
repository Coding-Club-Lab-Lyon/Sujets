
from model.model import Model

mon_modele = Model()
mon_modele.load("mon_modele.model")

maison = (
    1, # Nombre de chambres
    2, # Nombre de salles de bain
    134, # Taille de la maison
)

result = mon_modele.forward(maison)
print(result)


