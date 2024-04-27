import tkinter as tk
import math
import random

from Vector2D import Vector2D
from Player import Player
from Asteroids import Asteroid

MAX_ASTEROIDS = 20


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
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)
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
        self.keys_pressed[event.keysym] = False

    def update_score(self) -> None:
        """
        Updates the score on the canvas.
        :return:
        """
        self.main_canvas.create_text(60, 15, text=f"Score: {self.score}", fill="white", font=("Arial", 16))

    def spawn_asteroids(self):
        """
        Spawns new asteroids.
        :return:
        """
        while len(self.astroids) < MAX_ASTEROIDS:
            position = Vector2D(random.uniform(0, self.root.winfo_width()), random.uniform(0, self.root.winfo_height()))

            while (math.hypot(self.player.position.x - position.x, self.player.position.y - position.y)
                   < self.player.size + 50):
                position = Vector2D(random.uniform(0, self.root.winfo_width()),
                                    random.uniform(0, self.root.winfo_height()))

            velocity = Vector2D(random.uniform(-1, 1), random.uniform(-1, 1))

            size = random.randint(10, 50)

            self.astroids.append(Asteroid(position, velocity, size, self.root.winfo_width(), self.root.winfo_height()))

    def asteroid_manager(self) -> None:
        """
        Manage collision detection and spawning of asteroids.
        :return:
        """
        for asteroid in self.astroids:
            if math.hypot(self.player.position.x - asteroid.position.x,
                          self.player.position.y - asteroid.position.y) < self.player.size + asteroid.size:
                self.is_game_over = True
                return

            for bullet in self.player.bullets:
                if math.hypot(bullet.position.x - asteroid.position.x,
                              bullet.position.y - asteroid.position.y) < bullet.length + asteroid.size:
                    self.astroids.remove(asteroid)
                    self.player.bullets.remove(bullet)
                    self.score += 100
                    break

        self.spawn_asteroids()
        self.root.after(50, self.asteroid_manager)

    def update(self) -> None:
        """
        Updates the game state.
        :return:
        """
        if self.keys_pressed.get("Escape") or self.keys_pressed.get("q"):
            self.root.quit()
        if self.keys_pressed.get("Up"):
            self.player.accelerate(1)
        if self.keys_pressed.get("Down"):
            self.player.accelerate(-1)
        if self.keys_pressed.get("Left"):
            self.player.rotate(-5)
        if self.keys_pressed.get("Right"):
            self.player.rotate(5)
        if self.keys_pressed.get("space"):
            self.player.shoot()

        if self.is_game_over:
            self.main_canvas.create_text(self.root.winfo_width() / 2, self.root.winfo_height() / 2, text="Game Over",
                                         fill="white", font=("Arial", 32))
            self.root.after(100, self.update)
        else:
            self.main_canvas.delete("all")
            self.update_score()
            self.player.update(self.main_canvas)
            for asteroid in self.astroids:
                asteroid.update(self.main_canvas)
            self.root.update()
            self.root.after(50, self.update)

    def run(self) -> None:
        """
        Entry point of the game.
        :return:
        """
        self.root.after(0, self.update)
        self.root.after(2000, self.asteroid_manager)
        self.root.mainloop()
