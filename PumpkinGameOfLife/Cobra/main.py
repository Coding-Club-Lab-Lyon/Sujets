"""
LE JEU DE LA VIE DES CITROUILLES 🎃
Atelier Python - Halloween

VERSION CORRIGÉE - SOLUTION COMPLÈTE

RÈGLES DU JEU DE LA VIE:
1. Une citrouille vivante avec 2 ou 3 voisines survit
2. Une citrouille vivante avec moins de 2 voisines meurt (solitude)
3. Une citrouille vivante avec plus de 3 voisines meurt (surpopulation)
4. Une case vide avec exactement 3 voisines donne naissance à une citrouille
"""

from wrapper import PumpkinGameOfLife, compter_voisins, creer_grille_vide


def calculer_prochaine_generation(grille_actuelle):
    """
    Calcule l'état de la grille à la prochaine génération
    
    Args:
        grille_actuelle: la grille actuelle (liste de listes avec 0 et 1)
    
    Returns:
        La nouvelle grille après application des règles
    """
    # Récupérer les dimensions de la grille
    hauteur = len(grille_actuelle)
    largeur = len(grille_actuelle[0])
    
    # Créer une nouvelle grille vide pour la prochaine génération
    nouvelle_grille = creer_grille_vide(largeur, hauteur)
    
    # Parcourir toutes les cases de la grille
    for ligne in range(hauteur):
        for colonne in range(largeur):
            # Compter les voisins de cette case
            voisins = compter_voisins(grille_actuelle, ligne, colonne)
            
            # Vérifier si la case actuelle contient une citrouille
            if grille_actuelle[ligne][colonne] == 1:
                # C'est une citrouille vivante
                # Règle de survie : 2 ou 3 voisins
                if voisins == 2 or voisins == 3:
                    nouvelle_grille[ligne][colonne] = 1  # La citrouille survit
                else:
                    nouvelle_grille[ligne][colonne] = 0  # La citrouille meurt
            else:
                # C'est une case vide
                # Règle de naissance : exactement 3 voisins
                if voisins == 3:
                    nouvelle_grille[ligne][colonne] = 1  # Une nouvelle citrouille naît
                else:
                    nouvelle_grille[ligne][colonne] = 0  # La case reste vide
    
    return nouvelle_grille


if __name__ == "__main__":
    jeu = PumpkinGameOfLife(largeur=40, hauteur=30, taille_cellule=20)
    jeu.lancer()