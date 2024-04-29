import tkinter as tk
import math

from Vector2D import Vector2D


class Bullet:
    """
    A class to represent a bullet.
    """
    def __init__(self, position: Vector2D, velocity: Vector2D, direction: int) -> None:
        """
        Constructs all the necessary attributes for the bullet object.
        :param position: position of the bullet
        :param velocity: velocity of the bullet
        :param direction: direction of the bullet
        """
        self.position = position
        self.velocity = velocity
        self.direction = direction
        self.length = 10

    def update(self, canvas: tk.Canvas) -> bool:
        """
        Updates the bullet's position and direction.
        :param canvas: canvas to draw the bullet
        :return: True if the bullet is within the canvas, False otherwise
        """
        rotated_direction = (self.direction + 90) % 360
        end_point = Vector2D(
            self.position.x + self.length * math.cos(math.radians(rotated_direction)),
            self.position.y + self.length * math.sin(math.radians(rotated_direction))
        )
        canvas.create_line(self.position.x, self.position.y, end_point.x, end_point.y, fill="white")
        self.position = Vector2D(
            (self.position.x + self.velocity.x),
            (self.position.y + self.velocity.y)
        )
        if (self.position.x < 0 or self.position.x > canvas.winfo_width() or
                self.position.y < 0 or self.position.y > canvas.winfo_height()):
            return False
        else:
            return True
