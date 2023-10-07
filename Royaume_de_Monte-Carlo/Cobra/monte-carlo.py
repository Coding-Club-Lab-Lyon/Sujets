from src.show import *

def main():
    NB_ESSAI = 10_000

    def simulation(nb_essai):
        nb_point_total = 0
        nb_point_in_circle = 0

        for _ in range(nb_essai):
            # On choisi au hasard notre abscisse entre 0 et 1
            x = my_random(0, 1)
            # On choisi au hasard notre ordonnée entre 0 et 1
            y = my_random(0, 1)

            nb_point_total += 1

            if x**2 + y**2 < 1:
                nb_point_in_circle += 1

        pi = nb_point_in_circle / nb_point_total * 4

        # Afficher l'approximation de PI
        print(pi)
        display_round(mode="animate")
    simulation(NB_ESSAI)


if __name__ == "__main__":
    main()
