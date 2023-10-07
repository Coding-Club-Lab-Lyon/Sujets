from src.show import *

def main():
    NB_ESSAI = ...

    def simulation(nb_essai):
        nb_point_total = 0
        nb_point_in_circle = 0

        for _ in range(...):
            # On choisi au hasard notre abscisse entre 0 et 1
            x = my_random(.., ..)
            # On choisi au hasard notre ordonnée entre 0 et 1
            y = my_random(.., ..)

            nb_point_total += 1

            if magic formula:
                nb_point_in_circle += 1

        pi = nb_point_in_circle / nb_point_total * 4

        # Afficher l'approximation de PI
        print(pi)
        display_round(mode="show")
    simulation(NB_ESSAI)


if __name__ == "__main__":
    main()
