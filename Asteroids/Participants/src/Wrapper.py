import tkinter as tk
import math
import random

from Vector2D import Vector2D
from Player import Player
from Asteroids import Asteroid

MAX_ASTEROIDS = 20
REFRESH_RATE = 25


# tips: Ce fichier est un peu plus complexe que les autres, il peux être interessant de le faire après avoir compris les autres fichiers
class Wrapper:
    """
    A class to represent the game wrapper.
    """
    def __init__(self, width: int = 800, height: int = 600):
        """
        Constructs all the necessary attributes for the game wrapper object.
        :param width: width of the game window
        :param height: height of the game window
        """
        self.player = Player(Vector2D(width / 2, height / 2), Vector2D(0, 0), 0, 1, width, height)
        self.score = 0
        self.astroids = []
        self.is_game_over = False

        self.root: tk.Tk = tk.Tk()
        self.root.title("Wrapper")
        self.root.geometry(f"{width}x{height}")
        self.root.resizable(False, False)
        # TODO: Utilise la méthode bind de root pour lier les événements clavier à on_key_press et on_key_release
        pass

        self.keys_pressed = {}

        self.main_canvas: tk.Canvas = tk.Canvas(self.root, width=width, height=height, bg="black")
        self.main_canvas.pack()

    def on_key_press(self, event: tk.Event) -> None:
        """
        Handles the key press event.
        :param event: tkinter event object
        :return:
        """
        self.keys_pressed[event.keysym] = True

    def on_key_release(self, event: tk.Event) -> None:
        """
        Handles the key release event.
        :param event: tkinter event object
        """
        # TODO: Modifier la data lié à la touche
        pass

    def update_score(self) -> None:
        """
        Updates the score on the canvas.
        :return:
        """
        # TODO: Créer un text pour afficher le score.
        #  tips: regarde les méthodes de canvas
        #  tips: les coordonnées sont (60, 15) pour une police de taille de 16
        pass

    def spawn_asteroids(self):
        """
        Spawns new asteroids.
        :return:
        """
        while len(self.astroids) < MAX_ASTEROIDS:
            # TODO: Calcul et fait apparaitre un ou des astéroides
            # les astéroides doivent apparaitre à une distance raisonnable du joueur
            # Cette fonction peut être compliquée car elle appelle à quelques notions de mathématiques.
            # Si les calculs ne sont pas clairs, n'hésite pas à demander de l'aide, c'est un atelier de programmation avant tout.
            pass

    def asteroid_manager(self) -> None:
        """
        Manage collision detection and spawning of asteroids.
        :return:
        """
        for asteroid in self.astroids:
            if math.hypot(self.player.position.x - asteroid.position.x,
                          self.player.position.y - asteroid.position.y) < self.player.size + asteroid.size:
                # TODO: Gérer la collision entre le joueur et un astéroide
                pass

            for bullet in self.player.bullets:
                if math.hypot(bullet.position.x - asteroid.position.x,
                              bullet.position.y - asteroid.position.y) < bullet.length + asteroid.size:
                    # TODO: Gérer la collision entre une balle et un astéroide
                    pass

        self.spawn_asteroids()
        self.root.after(REFRESH_RATE, self.asteroid_manager)

    def update(self) -> None:
        """
        Updates the game state.
        :return:
        """
        if self.keys_pressed.get("Escape") or self.keys_pressed.get("q"):
            self.root.quit()
        # TODO: Gère les events clavier pour les touches "Up", "Down", "Left", "Right" et "space"
        pass

        if self.is_game_over:
            self.main_canvas.create_text(self.root.winfo_width() / 2, self.root.winfo_height() / 2, text="Game Over",
                                         fill="white", font=("Arial", 32))
            self.root.after(100, self.update)
        else:
            # TODO: Met à jour le jeu:
            # - canvas
            # - score
            # - joueur
            # - astéroides
            pass
            self.root.after(REFRESH_RATE, self.update)

    def run(self) -> None:
        """
        Entry point of the game.
        :return:
        """
        self.root.after(0, self.update)
        self.root.after(2000, self.asteroid_manager)
        self.root.mainloop()
