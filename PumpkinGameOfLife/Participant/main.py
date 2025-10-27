from wrapper import PumpkinGameOfLife, compter_voisins


def calculer_prochaine_generation(grille_actuelle):
    nouvelle_grille = grille_actuelle
    return nouvelle_grille


# ============================================================================
# CODE DE DÉMARRAGE - NE PAS MODIFIER
# ============================================================================

if __name__ == "__main__":
    jeu = PumpkinGameOfLife(largeur=40, hauteur=30, taille_cellule=20)
    jeu.lancer()