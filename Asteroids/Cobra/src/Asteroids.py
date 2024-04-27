import tkinter as tk

from Vector2D import Vector2D


class Asteroid:
    """
    A class to represent an asteroid.
    """
    def __init__(self, position: Vector2D, velocity: Vector2D, size: int, screen_width: int = 800,
                 screen_height: int = 600) -> None:
        """
        Constructs all the necessary attributes for the asteroid object.
        :param position: position of the asteroid
        :param velocity: velocity of the asteroid
        :param size: size of the asteroid representation
        :param screen_width: width of the screen
        :param screen_height: height of the screen
        """
        self.position = position
        self.velocity = velocity
        self.size = size
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, canvas: tk.Canvas) -> None:
        """
        Updates the asteroid's position.
        :param canvas: canvas to draw the asteroid
        """
        self.position = Vector2D((self.position.x + self.velocity.x) % self.screen_width,
                                 (self.position.y + self.velocity.y) % self.screen_height)
        canvas.create_oval(
            self.position.x - self.size, self.position.y - self.size,
            self.position.x + self.size, self.position.y + self.size,
            fill="white"
        )
